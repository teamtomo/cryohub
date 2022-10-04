import numpy as np
import pandas as pd
from cryotypes.poseset import PoseSetDataLabels as PSDL
from cryotypes.poseset import validate_poseset_dataframe
from scipy.spatial.transform import Rotation

from ..utils.constants import Relion
from ..utils.generic import guess_name


def read_box(
    path,
    name_regex=None,
    **kwargs,
):
    coords = np.loadtxt(path)
    rot = Rotation.identity(len(coords)).as_euler(Relion.EULER)
    name = guess_name(path, name_regex)

    df = pd.DataFrame(
        {
            PSDL.POSITION: coords,
            PSDL.ORIENTATION: rot,
            PSDL.EXPERIMENT_ID: name,
        }
    )
    return validate_poseset_dataframe(df, coerce=True)
