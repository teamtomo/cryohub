import pandas as pd
import starfile

from ..utils.constants import Relion


def write_star(coords, rot, file_path, features=None, overwrite=False):
    """
    write particle data to disk as a .star file
    """
    df = pd.DataFrame()
    df[Relion.COORD_HEADERS] = coords
    df[Relion.EULER_HEADERS] = rot.as_euler(Relion.EULER)
    if features is not None:
        df = pd.concat([df, features], axis=1)

    if not file_path.endswith('.star'):
        file_path = str(file_path) + '.star'
    starfile.write(df, file_path, overwrite=overwrite)
