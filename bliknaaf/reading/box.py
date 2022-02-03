import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation

from ..utils.generic import guess_name
from ..utils.euler import RELION_EULER


def read_box(
    path,
    name_regex=None,
    **kwargs,
):
    coords = np.loadtxt(path)
    rot = Rotation.identity(len(coords)).as_euler(RELION_EULER)
    name = guess_name(path, name_regex)
    df = pd.DataFrame()
    return coords, rot, {'name': name}
