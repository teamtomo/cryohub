import numpy as np
import pandas as pd
import starfile
from scipy.spatial.transform import Rotation

from naaf.reading.star import read_star
from naaf.data import Particles
from naaf.utils.constants import Relion


def test_read_relion30_3d(tmp_path):
    df = pd.DataFrame({
        'rlnCoordinateX': [1, 1],
        'rlnCoordinateY': [2, 2],
        'rlnCoordinateZ': [3, 3],
        'rlnOriginX': [0.1, 0.1],
        'rlnOriginY': [0.2, 0.2],
        'rlnOriginZ': [0.3, 0.3],
        'rlnAngleRot': [0, 0],
        'rlnAngleTilt': [0, 90],
        'rlnAnglePsi': [90, 0],
        'rlnMicrographName': ['a', 'b'],
        'feature': ['x', 'y'],
    })
    file_path = tmp_path / 'test.star'
    starfile.write(df, file_path)

    particles = read_star(file_path, name_regex=r'\w')
    part = particles[0]

    expected = Particles(
        name='a',
        coords=np.array([[0.9, 1.8, 2.7]]),
        rot=Rotation.from_euler(Relion.EULER, [[0, 0, 90]]),
        features=pd.DataFrame({'feature': ['x']})
    )
    assert expected == part



def test_read_relion31_3d(tmp_path):
    df_optics = pd.DataFrame({
        'rlnOpticsGroup': [1],
        'rlnImagePixelSize': [10],
    })
    df_particles = pd.DataFrame({
        'rlnCoordinateX': [1, 1],
        'rlnCoordinateY': [2, 2],
        'rlnCoordinateZ': [3, 3],
        'rlnOriginXAngst': [0.1, 0.1],
        'rlnOriginYAngst': [0.2, 0.2],
        'rlnOriginZAngst': [0.3, 0.3],
        'rlnAngleRot': [0, 0],
        'rlnAngleTilt': [0, 90],
        'rlnAnglePsi': [90, 0],
        'rlnMicrographName': ['a', 'b'],
        'feature': ['x', 'y'],
        'rlnOpticsGroup': [1, 1],
    })
    data_dict = {'optics': df_optics, 'particles': df_particles}
    file_path = tmp_path / 'test.star'
    starfile.write(data_dict, file_path)

    particles = read_star(file_path, name_regex=r'\w')
    part = particles[0]

    expected = Particles(
        name='a',
        pixel_size=10,
        coords=np.array([[0.99, 1.98, 2.97]]),
        rot=Rotation.from_euler(Relion.EULER, [[0, 0, 90]]),
        features=pd.DataFrame({'feature': ['x']})
    )
    assert expected == part
