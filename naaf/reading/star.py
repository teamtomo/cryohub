import numpy as np
import pandas as pd
import starfile
from cryotypes.poseset import PoseSetDataLabels as PSDL
from cryotypes.poseset import validate_poseset_dataframe
from scipy.spatial.transform import Rotation

from ..utils.constants import Relion
from ..utils.generic import ParseError, guess_name_vec


def construct_poseset(
    df,
    coord_headers,
    shift_headers,
    pixel_size_headers,
    exp_header,
    star_path,
    rescale_shifts=False,
    name_regex=None,
    guess_id=True,
):
    coords = np.asarray(df.get(coord_headers, 0), dtype=float)
    ndim = len(coord_headers)
    shifts = np.asarray(df.get(shift_headers, 0), dtype=float)

    pixel_size = df.get(pixel_size_headers, None)
    if pixel_size is not None:
        pixel_size = np.asarray(pixel_size, dtype=float)
        # XXX TODO: remove the following and support variable pixel sizes?
        pixel_size = pixel_size.ravel()[0]
        if rescale_shifts:
            shifts = shifts / pixel_size
    elif rescale_shifts:
        raise ParseError(
            "pixel size information is missing, but it is required because shifts are in Angstroms!"
        )

    if Relion.EULER_HEADERS[0] in df.columns:
        euler_convention = Relion.EULER
        eulers = np.asarray(df.get(Relion.EULER_HEADERS, 0), dtype=float)
    else:
        euler_convention = Relion.INPLANE
        eulers = np.asarray(df.get(Relion.EULER_HEADERS[2], 0), dtype=float)

    rot = Rotation.from_euler(euler_convention, eulers, degrees=True)

    # we want the inverse, which when applied to basis vectors it gives us the particle orientation
    rot = rot.inv()

    features = df.drop(columns=Relion.REDUNDANT_HEADERS, errors="ignore")

    exp_id = df[exp_header]
    if guess_id:
        exp_id = guess_name_vec(exp_id, name_regex)

    data = pd.DataFrame()
    data[PSDL.POSITION[:ndim]] = coords
    data[PSDL.SHIFT[:ndim]] = -shifts  # relion subtracts from coords
    data[PSDL.ORIENTATION] = np.asarray(rot)
    data[PSDL.PIXEL_SPACING] = pixel_size or 0
    data[PSDL.EXPERIMENT_ID] = exp_id
    data[PSDL.SOURCE] = star_path
    data = pd.concat([data, features], axis=1)

    return validate_poseset_dataframe(data, coerce=True)


def parse_relion_star(
    df,
    star_path="",
    name_regex=None,
    guess_id=True,
    **kwargs,
):
    # find out which columns are present and which version we're dealing with
    rescale_shifts = True

    if Relion.PIXEL_SIZE_HEADER["3.1"] in df.columns:
        # 3.1 has priority over 4 (cause it's still used in 4 for single particle)
        version = "3.1"
    elif Relion.PIXEL_SIZE_HEADER["4.0"] in df.columns:
        version = "4.0"
    else:
        # also includes if this is not present (required for later versions!)
        version = "3.0"
        rescale_shifts = False

    pixel_size_headers = Relion.PIXEL_SIZE_HEADER[version]
    shift_headers = Relion.SHIFT_HEADERS[version]

    if (
        Relion.COORD_HEADERS[0] not in df.columns
        or Relion.COORD_HEADERS[1] not in df.columns
    ):
        raise ParseError("coordinate information missing")
    elif Relion.COORD_HEADERS[-1] in df.columns:
        coord_headers = Relion.COORD_HEADERS
    else:
        coord_headers = Relion.COORD_HEADERS[:2]
        shift_headers = shift_headers[:2]

    # start parsing
    if Relion.MICROGRAPH_NAME_HEADER[version] in df.columns:
        exp_header = Relion.MICROGRAPH_NAME_HEADER[version]
    else:
        exp_header = None

    return construct_poseset(
        df,
        coord_headers,
        shift_headers,
        pixel_size_headers,
        exp_header,
        star_path,
        rescale_shifts=rescale_shifts,
        name_regex=name_regex,
        guess_id=guess_id,
    )


def read_star(star_path, **kwargs):
    try:
        raw_data = starfile.read(star_path, always_dict=True)
    except pd.errors.EmptyDataError:  # raised sometimes by .star files with completely different data
        raise ParseError(f"the contents of {star_path} have the wrong format")

    if len(raw_data) == 1:
        df = list(raw_data.values())[0]
    elif "particles" in raw_data and "optics" in raw_data:
        df = raw_data["particles"].merge(
            raw_data["optics"], on=Relion.OPTICS_GROUP_HEADER
        )
    else:
        raise ParseError(
            f"Failed to parse {star_path} as particles. Are you sure this is a particle file?"
        )

    return parse_relion_star(df, star_path=star_path, **kwargs)
