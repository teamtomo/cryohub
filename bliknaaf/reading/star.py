import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation
import starfile

from ..utils.generic import guess_name, ParseError
from ..utils.euler import RELION_EULER, RELION_PSI


COORD_HEADERS = [f'rlnCoordinate{axis}' for axis in 'XYZ']
EULER_HEADERS = {
    3: [f'rlnAngle{angle}' for angle in ('Rot', 'Tilt', 'Psi')],
    2: ['rlnAnglePsi']
}
SHIFT_HEADERS = {
    '3.0': [f'rlnOrigin{axis}' for axis in 'XYZ'],
    '3.1': [f'rlnOrigin{axis}Angst' for axis in 'XYZ']
}

PIXEL_SIZE_HEADERS = {
    '3.0': ['rlnDetectorPixelSize'],
    '3.1': ['rlnImagePixelSize']
}
MICROGRAPH_NAME_HEADER = 'rlnMicrographName'

ALL_HEADERS = (
    COORD_HEADERS +
    EULER_HEADERS[3] +
    SHIFT_HEADERS['3.0'] +
    SHIFT_HEADERS['3.1'] +
    PIXEL_SIZE_HEADERS['3.0'] +
    PIXEL_SIZE_HEADERS['3.1']
)


def extract_data(
    df,
    mode='3.1',
    name_regex=None,
    star_path='',
):
    """
    extract particle data from a starfile dataframe
    """
    if COORD_HEADERS[-1] in df.columns:
        dim = 3
    else:
        dim = 2

    if MICROGRAPH_NAME_HEADER in df.columns:
        groups = df.groupby(MICROGRAPH_NAME_HEADER)
    else:
        groups = [(star_path, df)]

    volumes = []
    for micrograph_name, df_volume in groups:
        name = guess_name(micrograph_name, name_regex)

        coords = df_volume[COORD_HEADERS[:dim]].to_numpy(dtype=float)

        pixel_size = np.asarray(df_volume.get(PIXEL_SIZE_HEADERS[mode], 1.0))

        if (shifts := df_volume.get(SHIFT_HEADERS[mode][:dim])) is not None:
            # only relion 3.1 has shifts in angstroms
            if mode == '3.1':
                shifts = shifts / pixel_size
            coords -= shifts

        eulers = np.asarray(df_volume.get(EULER_HEADERS[dim], 0))
        if dim == 3:
            rot = Rotation.from_euler(RELION_EULER, eulers)
        else:
            rot = Rotation.from_euler(RELION_PSI, eulers)

        features = pd.DataFrame({
            key: df_volume[key].to_numpy()
            for key in df.columns
            if key not in ALL_HEADERS
        })

        # TODO: better way to handle pizel size? Now we can only account for uniform size
        volumes.append((coords, rot, {'features': features, 'pixel_size': pixel_size, 'name': name}))

    return volumes


def parse_relion30(raw_data, **kwargs):
    """
    Attempt to parse raw data dict from starfile.read as a RELION 3.0 style star file
    """
    if len(raw_data.values()) > 1:
        raise ParseError("Cannot parse as RELION 3.0 format STAR file")

    df = list(raw_data.values())[0]
    return extract_data(df, mode='3.0', **kwargs)


def parse_relion31(raw_data, **kwargs):
    """
    Attempt to parse raw data from starfile.read as a RELION 3.1 style star file
    """
    if list(raw_data.keys()) != ['optics', 'particles']:
        raise ParseError("Cannot parse as RELION 3.1 format STAR file")

    df = raw_data['particles'].merge(raw_data['optics'])
    return extract_data(df, mode='3.1', **kwargs)


reader_functions = {
    'relion_3.0': parse_relion30,
    'relion_3.1': parse_relion31,
}


def read_star(star_path, **kwargs):
    """
    Dispatch function for reading a starfile into one or multiple ParticleBlocks
    """
    try:
        raw_data = starfile.read(star_path, always_dict=True)
    except pd.errors.EmptyDataError:  # raised sometimes by .star files with completely different data
        raise ParseError(f'the contents of {star_path} have the wrong format')

    failed_reader_functions = []
    for style, reader_function in reader_functions.items():
        try:
            particle_blocks = reader_function(raw_data, star_path=star_path, **kwargs)
            return particle_blocks
        except ParseError:
            failed_reader_functions.append((style, reader_function))
    raise ParseError(f'Failed to parse {star_path} using {failed_reader_functions}')
