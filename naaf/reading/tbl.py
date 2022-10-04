import dynamotable
import numpy as np
import pandas as pd
from cryotypes.poseset import PoseSetDataLabels as PSDL
from cryotypes.poseset import validate_poseset_dataframe
from scipy.spatial.transform import Rotation

from ..utils.constants import Dynamo
from ..utils.generic import guess_name_vec


def read_tbl(table_path, table_map_file=None, guess_id=True, name_regex=None, **kwargs):
    """
    Read particles from a dynamo format table file
    """
    df = dynamotable.read(table_path, table_map_file)

    if Dynamo.EXP_NAME_HEADER in df.columns:
        exp_id = df[Dynamo.EXP_NAME_HEADER]
        if guess_id:
            exp_id = guess_name_vec(exp_id, name_regex)
    else:
        exp_id = df[Dynamo.EXP_ID_HEADER].astype(str)

    if Dynamo.COORD_HEADERS[-1] in df.columns:
        ndim = 3
    else:
        ndim = 2

    coords = np.asarray(df[Dynamo.COORD_HEADERS[:ndim]], dtype=float)
    shifts = np.asarray(df.get(Dynamo.SHIFT_HEADERS[:ndim], 0), dtype=float)
    eulers = np.asarray(df.get(Dynamo.EULER_HEADERS[ndim], 0), dtype=float)

    if ndim == 3:
        rot = Rotation.from_euler(Dynamo.EULER, eulers, degrees=True)
    else:
        rot = Rotation.from_euler(Dynamo.INPLANE, eulers, degrees=True)

    # we want the inverse, which when applied to basis vectors it gives us the particle orientation
    rot = rot.inv()

    features = df.drop(columns=Dynamo.REDUNDANT_HEADERS, errors="ignore")

    data = pd.DataFrame()
    data[PSDL.POSITION[:ndim]] = coords
    data[PSDL.SHIFT[:ndim]] = shifts
    data[PSDL.ORIENTATION] = np.asarray(rot)
    data[PSDL.EXPERIMENT_ID] = exp_id
    data[PSDL.SOURCE] = table_path
    data = pd.concat([data, features], axis=1)

    return validate_poseset_dataframe(data, coerce=True)
