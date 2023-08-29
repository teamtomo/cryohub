import dynamotable
import numpy as np
from cryotypes.poseset import validate_poseset
from scipy.spatial.transform import Rotation

from ..utils.constants import Dynamo
from ..utils.generic import get_columns_or_default
from ..utils.types import PoseSet


def read_tbl(table_path, table_map_file=None, name_regex=None, **kwargs):
    """
    Read particles from a dynamo format table file
    """
    df = dynamotable.read(table_path, table_map_file)

    if Dynamo.EXP_NAME_HEADER is df.columns:
        groups_by_exp = [(None, df)]
    else:
        groups_by_exp = df.groupby(Dynamo.EXP_ID_HEADER)

    posesets = []
    for exp_id, exp_df in groups_by_exp:
        exp_df = exp_df.reset_index(drop=True)
        coords = get_columns_or_default(exp_df, Dynamo.COORD_HEADERS)
        shifts = get_columns_or_default(exp_df, Dynamo.SHIFT_HEADERS)
        eulers = get_columns_or_default(exp_df, Dynamo.EULER_HEADERS[3])

        if eulers is None or np.allclose(eulers, 0):
            rot = None
        else:
            if all(header in exp_df.columns for header in Dynamo.EULER_HEADERS[3]):
                euler_convention = Dynamo.EULER
            else:
                euler_convention = Dynamo.INPLANE
                eulers = eulers[:, Dynamo.EULER_HEADERS[2]]
            rot = Rotation.from_euler(euler_convention, eulers, degrees=True)

            # we want the inverse, which when applied to basis vectors it gives us the particle orientation
            rot = rot.inv()

        features = exp_df.drop(columns=Dynamo.REDUNDANT_HEADERS, errors="ignore")

        poseset = PoseSet(
            position=coords,
            shift=shifts,
            orientation=rot,
            experiment_id=exp_id,
            source=table_path,
            features=features,
        )

        posesets.append(validate_poseset(poseset, coerce=True))

    return posesets
