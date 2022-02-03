import numpy as np
from scipy.spatial.transform import Rotation
import dynamotable

from ..utils.generic import guess_name
from ..utils.euler import DYNAMO_EULER, DYNAMO_TILT


COORD_HEADERS = ['x', 'y', 'z']
SHIFT_HEADERS = ['dx', 'dy', 'dz']
EULER_HEADERS = {
    3: ['tdrot', 'tilt', 'narot'],
    2: ['tilt']  # TODO: 2d column name might be wrong!
}

ALL_HEADERS = COORD_HEADERS + SHIFT_HEADERS + EULER_HEADERS[3]


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
    pixel_size=None,
    **kwargs
):
    """
    Read particles from a dynamo format table file
    """
    df = dynamotable.read(table_path, table_map_file)

    split_on = 'tomo'
    if 'tomo_file' in df.columns:
        split_on = 'tomo_file'

    if COORD_HEADERS[-1] in df.columns:
        dim = 3
    else:
        dim = 2

    volumes = []
    for volume, df_volume in df.groupby(split_on):
        name = name_from_volume(volume, name_regex)
        coords = np.asarray(df_volume[COORD_HEADERS[:dim]])
        if (shifts := df_volume.get(SHIFT_HEADERS[:dim])) is not None:
            coords += shifts

        eulers = np.asarray(df_volume.get(EULER_HEADERS[dim]))
        if dim == 3:
            rot = Rotation.from_euler(DYNAMO_EULER, eulers)
        else:
            rot = Rotation.from_euler(DYNAMO_TILT, eulers)

        features = {
            key: df_volume[key].to_numpy()
            for key in df.columns
            if key not in ALL_HEADERS
        }

        if pixel_size is None:
            pixel_size = 1

        volumes.append((coords, rot, {'features': features, 'pixel_size': pixel_size, 'name': name}))

    return volumes
