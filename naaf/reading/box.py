import numpy as np
from scipy.spatial.transform import Rotation

from ..data import Particles
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

    return Particles(
        coords=coords,
        rot=rot,
        name=name,
    )
