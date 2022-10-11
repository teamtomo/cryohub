import dynamotable
import numpy as np
import pandas as pd
from cryotypes.poseset import PoseSetDataLabels as PSDL
from scipy.spatial.transform import Rotation

from ..utils.constants import Dynamo


def write_tbl(particles, file_path):
    """
    write particle data to disk as a dynamo .tbl file
    """
    ndim = 3 if PSDL.POSITION_Z in particles.columns else 2

    df = pd.DataFrame()
    df[Dynamo.COORD_HEADERS[:ndim]] = particles[PSDL.POSITION[:ndim]]
    df[Dynamo.SHIFT_HEADERS[:ndim]] = particles[PSDL.SHIFT[:ndim]]

    rot = Rotation.concatenate(particles[PSDL.ORIENTATION]).inv()  # invert back
    eulers = rot.as_euler(Dynamo.EULER, degrees=True)
    if np.allclose(eulers[:, 1:], 0):
        # single angle world
        df[Dynamo.EULER_HEADERS[2]] = eulers[:, 0]
    else:
        df[Dynamo.EULER_HEADERS[3]] = eulers

    df[Dynamo.EXP_ID_HEADER] = particles[PSDL.EXPERIMENT_ID]

    if not str(file_path).endswith(".tbl"):
        file_path = str(file_path) + ".tbl"
    dynamotable.write(df, file_path)
