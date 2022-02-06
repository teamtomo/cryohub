import pandas as pd
import starfile

from ..utils.constants import Relion


def write_star(particles, file_path, features=None, overwrite=False):
    """
    write particle data to disk as a .star file
    """
    df = pd.DataFrame()
    df[Relion.COORD_HEADERS] = particles.coords
    df[Relion.EULER_HEADERS[3]] = particles.rot.as_euler(Relion.EULER, degrees=True)
    if particles.pixel_size is not None:
        df[Relion.PIXEL_SIZE_HEADERS['3.1']] = particles.pixel_size
    if particles.features is not None:
        df = pd.concat([df, features], axis=1)

    if not str(file_path).endswith('.star'):
        file_path = str(file_path) + '.star'
    starfile.write(df, file_path, overwrite=overwrite)
