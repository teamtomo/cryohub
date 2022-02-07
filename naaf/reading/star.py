import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation
import starfile

from ..utils.generic import guess_name, ParseError
from ..utils.constants import Naaf, Relion
from ..data import Particles


def extract_data(
    df,
    mode='3.1',
    name_regex=None,
    star_path='',
    **kwargs,
):
    """
    extract particle data from a starfile dataframe
    """
    if Relion.COORD_HEADERS[-1] in df.columns:
        dim = 3
    else:
        dim = 2

    if Relion.MICROGRAPH_NAME_HEADER in df.columns:
        groups = df.groupby(Relion.MICROGRAPH_NAME_HEADER)
    else:
        groups = [(star_path, df)]

    particles = []
    for micrograph_name, df_volume in groups:
        name = guess_name(micrograph_name, name_regex)

        coords = np.asarray(df_volume[Relion.COORD_HEADERS[:dim]], dtype=float)
        shifts = np.asarray(df_volume.get(Relion.SHIFT_HEADERS[mode][:dim], 0), dtype=float)

        pixel_size = df_volume.get(Relion.PIXEL_SIZE_HEADERS[mode])
        if pixel_size is not None:
            pixel_size = np.asarray(pixel_size, dtype=float)
            # XXX TODO: remove the following and support variable pixel sizes?
            pixel_size = pixel_size.ravel()[0]

        # only relion 3.1 has shifts in angstroms
        if mode == '3.1':
            if pixel_size is None:
                raise ParseError(f'Detected Relion 3.1 format, but no pixel size data!')
            shifts = shifts / pixel_size

        coords -= shifts

        eulers = np.asarray(df_volume.get(Relion.EULER_HEADERS[dim], 0), dtype=float)
        if dim == 3:
            rot = Rotation.from_euler(Relion.EULER, eulers, degrees=True)
        else:
            rot = Rotation.from_euler(Relion.INPLANE, eulers, degrees=True)

        # we want the inverse, which when applied to basis vectors it gives us the particle orientation
        rot = rot.inv()

        features = df_volume.drop(columns=Relion.ALL_HEADERS, errors='ignore')

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
