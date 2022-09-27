import numpy as np
import pandas as pd
import starfile
from scipy.spatial.transform import Rotation

from ..data import Particles
from ..utils.constants import Naaf, Relion
from ..utils.generic import ParseError, guess_name


def parse_groups(
    groups,
    coord_headers,
    shift_headers,
    pixel_size_headers,
    euler_convention,
    rescale_shifts=False,
    name_regex=None,
):
    particles = []

    for micrograph_name, df_volume in groups:
        # drop global index to prevent issues with concatenation and similar
        df_volume = df_volume.reset_index(drop=True)

        name = guess_name(micrograph_name, name_regex)

        coords = np.asarray(df_volume.get(coord_headers, 0), dtype=float)
        shifts = np.asarray(df_volume.get(shift_headers, 0), dtype=float)

        pixel_size = df_volume.get(pixel_size_headers, None)
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

        coords -= shifts

        # always work with 3D, add z=0
        if coords.shape[-1] == 2:
            coords = np.pad(coords, ((0, 0), (0, 1)))

        eulers = np.asarray(df_volume.get(Relion.EULER_HEADERS, 0), dtype=float)
        rot = Rotation.from_euler(euler_convention, eulers, degrees=True)

        # we want the inverse, which when applied to basis vectors it gives us the particle orientation
        rot = rot.inv()

        features = df_volume.drop(columns=Relion.ALL_HEADERS, errors="ignore")

        data = pd.DataFrame()
        data[Naaf.COORD_HEADERS] = coords
        data[Naaf.ROT_HEADER] = np.asarray(rot)
        data = pd.concat([data, features], axis=1)

        particles.append(
            Particles(
                data=data,
                pixel_size=pixel_size,
                name=name,
            )
        )

    return particles


def parse_relion_star(
    df,
    name_regex=None,
    star_path="",
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

    if Relion.EULER_HEADERS[0] in df.columns:
        euler_convention = Relion.EULER
    else:
        euler_convention = Relion.INPLANE

    # start parsing
    if Relion.MICROGRAPH_NAME_HEADER[version] in df.columns:
        groups = df.groupby(Relion.MICROGRAPH_NAME_HEADER[version])
    else:
        groups = [(star_path, df)]

    return parse_groups(
        groups,
        coord_headers,
        shift_headers,
        pixel_size_headers,
        euler_convention,
        rescale_shifts,
        name_regex=name_regex,
    )


def read_star(star_path, **kwargs):
    try:
        raw_data = starfile.read(star_path, always_dict=True)
    except pd.errors.EmptyDataError:  # raised sometimes by .star files with completely different data
        raise ParseError(f"the contents of {star_path} have the wrong format")

    if len(raw_data) == 1:
        df = list(raw_data.values())[0]
    elif "particles" in raw_data and "optics" in raw_data:
        df = raw_data["particles"].merge(raw_data["optics"])
    else:
        raise ParseError(
            f"Failed to parse {star_path} as particles. Are you sure this is a particle file?"
        )

    return parse_relion_star(df, star_path=star_path, **kwargs)
