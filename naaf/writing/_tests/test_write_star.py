import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation

from naaf.writing.star import write_star
from naaf.data import Particles
from naaf.utils.constants import Naaf


def test_write_star(tmp_path):
    file_path = tmp_path / 'test.star'
    data = pd.DataFrame()
    data[Naaf.COORD_HEADERS] = np.ones((2, 3))
    data[Naaf.ROT_HEADER] = np.asarray(Rotation.identity(2))
    data['feature'] = ['x', 'y']

    particle = Particles(
        data=data,
        name='test',
    )

    write_star(particle, file_path)
