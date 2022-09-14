import numpy as np
import pandas as pd
from cryopose import CryoPoseDataLabels as CPDL
from scipy.spatial.transform import Rotation

from naaf.data import Particles
from naaf.writing.star import write_star


def test_write_star(tmp_path):
    file_path = tmp_path / "test.star"
    data = pd.DataFrame()
    data[CPDL.POSITION] = np.ones((2, 3))
    data[CPDL.ORIENTATION] = np.asarray(Rotation.identity(2))
    data["feature"] = ["x", "y"]

    particle = Particles(
        data=data,
        name="test",
    )

    write_star(particle, file_path)
