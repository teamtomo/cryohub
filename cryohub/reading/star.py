import numpy as np
import pandas as pd
import starfile
from cryotypes.poseset import validate_poseset
from scipy.spatial.transform import Rotation

from ..utils.constants import Relion
from ..utils.generic import ParseError, get_columns_or_default, guess_name
from ..utils.star import merge_optics
from ..utils.types import PoseSet


def construct_poseset(
    df,
    coord_headers,
    shift_headers,
    pixel_size_headers,
    star_path,
    exp_id,
    rescale_shift=False,
    name_regex=None,
):
    coords = get_columns_or_default(df, coord_headers)
    shift = get_columns_or_default(df, shift_headers)
    # relion shift subtract from coordinates
    if shift is not None:
        shift = -shift

    pixel_size = get_columns_or_default(df, pixel_size_headers)
    if pixel_size is not None:
        pixel_size = np.asarray(pixel_size, dtype=float)
        # XXX TODO: remove the following and support variable pixel sizes?
        pixel_size = pixel_size.ravel()[0] or 1  # if zero we get a bunch of nans
        if rescale_shift and shift is not None:
            shift = shift / pixel_size
    elif rescale_shift:
        raise ParseError(
            "pixel size information is missing, but it is required because shift are in Angstroms!"
        )

    eulers = get_columns_or_default(df, Relion.EULER_HEADERS)
    if eulers is None or np.allclose(eulers, 0):
        rot = None
    else:
        if Relion.EULER_HEADERS[0] in df.columns:
            euler_convention = Relion.EULER
        else:
            euler_convention = Relion.INPLANE
            eulers = eulers[:, 2]
        rot = Rotation.from_euler(euler_convention, eulers, degrees=True)

        # we want the inverse, which when applied to basis vectors it gives us the particle orientation
        rot = rot.inv()

    exp_id = guess_name(exp_id, name_regex)

    features = df.drop(columns=Relion.REDUNDANT_HEADERS, errors="ignore")

    poseset = PoseSet(
        position=coords,
        shift=shift,
        orientation=rot,
        pixel_spacing=pixel_size or 0,
        experiment_id=exp_id,
        source=star_path,
        features=features,
    )

    return validate_poseset(poseset, coerce=True)


def get_proper_header_version(df, header_dict):
    for headers in header_dict.values():
        if isinstance(headers, str):
            if headers in df.columns:
                return headers
        elif any(col in df.columns for col in headers):
            return headers
    return None


def parse_relion_star(
    df,
    star_path="",
    name_regex=None,
    **kwargs,
):
    # find out which columns are present and which version we're dealing with
    rescale_shift = True

    pixel_size_headers = (
        get_proper_header_version(df, Relion.PIXEL_SIZE_HEADER)
        or Relion.PIXEL_SIZE_HEADER["3.0"]
    )
    if pixel_size_headers == Relion.PIXEL_SIZE_HEADER["3.0"]:
        rescale_shift = False

    shift_headers = get_proper_header_version(df, Relion.SHIFT_HEADERS)

    if (
        Relion.COORD_HEADERS[0] not in df.columns
        or Relion.COORD_HEADERS[1] not in df.columns
    ):
        raise ParseError("coordinate information missing")

    coord_headers = Relion.COORD_HEADERS
    exp_header = get_proper_header_version(df, Relion.MICROGRAPH_NAME_HEADER)
    # maybe it has experiment_id column from previous write
    if exp_header is None:
        exp_header = "experiment_id" if "experiment_id" in df.columns else None

    if exp_header is None:
        groups_by_exp = [(None, df)]
    else:
        groups_by_exp = df.groupby(exp_header)

    return [
        construct_poseset(
            exp_df.reset_index(drop=True),
            coord_headers=coord_headers,
            shift_headers=shift_headers,
            pixel_size_headers=pixel_size_headers,
            star_path=star_path,
            exp_id=exp_id,
            rescale_shift=rescale_shift,
            name_regex=name_regex,
        )
        for exp_id, exp_df in groups_by_exp
    ]


def read_star(star_path, **kwargs):
    try:
        raw_data = starfile.read(star_path, always_dict=True)
    except (
        pd.errors.EmptyDataError
    ):  # raised sometimes by .star files with completely different data
        raise ParseError(f"the contents of {star_path} have the wrong format")

    if len(raw_data) == 1:
        df = list(raw_data.values())[0]
    elif "particles" in raw_data and "optics" in raw_data:
        df = merge_optics(raw_data)
    else:
        raise ParseError(
            f"Failed to parse {star_path} as particles. Are you sure this is a particle file?"
        )

    return parse_relion_star(df, star_path=star_path, **kwargs)
