import numpy as np
from scipy.spatial.transform import Rotation
import dynamotable

from ..utils.generic import guess_name
from ..utils.constants import Dynamo
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

    data = []
    for volume, df_volume in df.groupby(split_on):
        name = name_from_volume(volume, name_regex)
        coords = np.asarray(df_volume[Dynamo.COORD_HEADERS[:dim]], dtype=float)
        shifts = np.asarray(df_volume.get(Dynamo.SHIFT_HEADERS[:dim], 0), dtype=float)
        # XXX TODO: Check if like the was with Relion there's an issue with + or - shifts!
        coords -= shifts

        eulers = np.asarray(df_volume.get(Dynamo.EULER_HEADERS[dim], 0), dtype=float)
        if dim == 3:
            rot = Rotation.from_euler(Dynamo.EULER, eulers)
        else:
            rot = Rotation.from_euler(Dynamo.INPLANE, eulers)

        data.append(
            Particles(
                coords=coords,
                rot=rot,
                name=name,
            )
        )

    return data
