import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation
import dynamotable

from ..utils.generic import guess_name
from ..utils.constants import Naaf, Dynamo
from ..data import Particles


def name_from_volume(volume_identifier, name_regex=None):
    """Generate ParticleBlock name from volume identifier from dataframe
    """
    if isinstance(volume_identifier, int):
        return str(volume_identifier)
    elif isinstance(volume_identifier, str):
        return guess_name(volume_identifier, name_regex)


def read_tbl(
    table_path,
    table_map_file=None,
    name_regex=None,
    **kwargs
):
    """
    Read particles from a dynamo format table file
    """
    df = dynamotable.read(table_path, table_map_file)

    split_on = 'tomo'
    if 'tomo_file' in df.columns:
        split_on = 'tomo_file'

    if Dynamo.COORD_HEADERS[-1] in df.columns:
        dim = 3
    else:
        dim = 2

    particles = []
    for volume, df_volume in df.groupby(split_on):
        name = name_from_volume(volume, name_regex)
        coords = np.asarray(df_volume[Dynamo.COORD_HEADERS[:dim]], dtype=float)
        shifts = np.asarray(df_volume.get(Dynamo.SHIFT_HEADERS[:dim], 0), dtype=float)
        coords += shifts

        eulers = np.asarray(df_volume.get(Dynamo.EULER_HEADERS[dim], 0), dtype=float)
        if dim == 3:
            rot = Rotation.from_euler(Dynamo.EULER, eulers, degrees=True)
        else:
            rot = Rotation.from_euler(Dynamo.INPLANE, eulers, degrees=True)

        # we want the inverse, which when applied to basis vectors it gives us the particle orientation
        rot = rot.inv()

        data = pd.DataFrame()
        data[Naaf.COORD_HEADERS] = coords
        data[Naaf.ROT_HEADER] = np.asarray(rot)

        particles.append(
            Particles(
                data=data,
                name=name,
            )
        )

    return particles
