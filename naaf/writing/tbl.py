import pandas as pd
import dynamotable

from ..utils.constants import Dynamo


def write_tbl(particles, file_path):
    """
    write particle data to disk as a dynamo .tbl file
    """
    df = pd.DataFrame()
    df[Dynamo.COORD_HEADERS] = particles.coords
    df[Dynamo.EULER_HEADERS[3]] = particles.rot.as_euler(Dynamo.EULER, degrees=True)

    if not str(file_path).endswith('.star'):
        file_path = str(file_path) + '.star'
    dynamotable.write(df, file_path)
