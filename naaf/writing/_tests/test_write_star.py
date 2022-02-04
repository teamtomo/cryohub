import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation

from naaf.writing.star import write_star
from naaf.data import Particles


def test_write_star(tmp_path):
    file_path = tmp_path / 'test.star'
    particle = Particles(
        coords=np.ones((2, 3)),
        rot=Rotation.identity(2),
        features=pd.DataFrame({'a': [1, 1]})
    )

    write_star(particle, file_path)
