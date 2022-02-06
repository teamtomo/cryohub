import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation

from naaf.writing.tbl import write_tbl
from naaf.data import Particles


def test_write_tbl(tmp_path):
    file_path = tmp_path / 'test.tbl'
    particle = Particles(
        coords=np.ones((2, 3)),
        rot=Rotation.identity(2),
        features=pd.DataFrame({'a': [1, 1]})
    )

    write_tbl(particle, file_path)

