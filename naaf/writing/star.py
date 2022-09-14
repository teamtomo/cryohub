import pandas as pd
import starfile
from cryopose import CryoPoseDataLabels as CPDL
from scipy.spatial.transform import Rotation

from ..utils.constants import Relion


def write_star(particles, file_path, features=None, overwrite=False):
    """
    write particle data to disk as a .star file
    """
    df = pd.DataFrame()
    df[Relion.COORD_HEADERS] = particles.data[CPDL.POSITION]
    rot = Rotation.concatenate(particles.data[CPDL.ORIENTATION])
    # we use the inverse rotation in naaf
    df[Relion.EULER_HEADERS] = rot.inv().as_euler(Relion.EULER, degrees=True)

    features = particles.data.drop(columns=Relion.ALL_HEADERS, errors="ignore")
    df = pd.concat([df, features], axis=1)

    if particles.pixel_size is not None:
        df[Relion.PIXEL_SIZE_HEADERS["3.1"]] = particles.pixel_size

    if not str(file_path).endswith(".star"):
        file_path = str(file_path) + ".star"
    starfile.write(df, file_path, overwrite=overwrite)
