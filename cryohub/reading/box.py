import numpy as np
from cryotypes.poseset import validate_poseset

from ..utils.generic import guess_name
from ..utils.types import PoseSet


def read_box(
    path,
    name_regex=None,
    **kwargs,
):
    coords = np.loadtxt(path)
    name = guess_name(path, name_regex)

    poseset = PoseSet(
        position=coords,
        experiment_id=name,
        source=path,
    )
    return validate_poseset(poseset, coerce=True)
