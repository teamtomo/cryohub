import numpy as np
import pandas as pd
import dynamotable
from scipy.spatial.transform import Rotation

from naaf.reading.tbl import read_tbl
from naaf.data import Particles
from naaf.utils.constants import Dynamo


def test_read_tbl(tmp_path):
    df = pd.DataFrame({
        'x': [1, 1],
        'y': [2, 2],
        'z': [3, 3],
        'dx': [0.1, 0.1],
        'dy': [0.2, 0.2],
        'dz': [0.3, 0.3],
        'tdrot': [0, 0],
        'tilt': [0, 90],
        'narot': [90, 0],
        'tomo': [0, 1],
    })
    file_path = tmp_path / 'test.tbl'
    dynamotable.write(df, file_path)

    particles = read_tbl(file_path, name_regex=r'\w')
    part = particles[0]

    expected = Particles(
        name='0',
        coords=np.array([[0.9, 1.8, 2.7]]),
        rot=Rotation.from_euler(Dynamo.EULER, [[0, 0, 90]], degrees=True),
    )

    assert expected == part
