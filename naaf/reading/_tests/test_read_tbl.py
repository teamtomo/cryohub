import numpy as np
import pandas as pd
import dynamotable
from scipy.spatial.transform import Rotation

from naaf.reading.tbl import read_tbl
from naaf.data import Particles
from naaf.utils.constants import Naaf, Dynamo
from naaf.utils.testing import assert_data_equal


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

    expected_data = pd.DataFrame()
    expected_data[Naaf.COORD_HEADERS] = np.array([[1.1, 2.2, 3.3]])
    expected_data[Naaf.ROT_HEADER] = Rotation.from_euler(Dynamo.EULER, [[0, 0, 90]], degrees=True).inv()

    expected = Particles(
        data=expected_data,
        name='0',
    )

    assert_data_equal(part, expected)
