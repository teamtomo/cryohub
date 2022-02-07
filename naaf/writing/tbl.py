import pandas as pd
from scipy.spatial.transform import Rotation
import dynamotable

from ..utils.constants import Naaf, Dynamo


def write_tbl(particles, file_path):
    """
    write particle data to disk as a dynamo .tbl file
    """
    df = pd.DataFrame()
    df[Dynamo.COORD_HEADERS] = particles.data[Naaf.COORD_HEADERS]
    rot = Rotation.concatenate(particles.data[Naaf.ROT_HEADER])
    # we use the inverse rotation in naaf
    df[Dynamo.EULER_HEADERS[3]] = rot.inv().as_euler(Dynamo.EULER, degrees=True)

    if not str(file_path).endswith('.star'):
        file_path = str(file_path) + '.star'
    dynamotable.write(df, file_path)
