import numpy as np
import pandas as pd
import pytest
from cryotypes.image import Image
from scipy.spatial.transform import Rotation

from .utils.types import PoseSet

# some real use case
_angles_relion = np.array(
    [[-18.20820, 138.764387, 10.931106], [-135.12769, 161.921662, -65.26683]]
)

_rotations = Rotation.from_euler("ZYZ", _angles_relion, degrees=True).inv()

_angles_dynamo = _rotations.inv().as_euler("zxz", degrees=True)


@pytest.fixture
def poseset():
    return (
        PoseSet(
            position=np.array([[1, 2, 3]]),
            shift=np.array([[0.01, 0.02, 0.03]]),
            orientation=_rotations[:1],
            experiment_id="a",
            pixel_spacing=10,
            source="test.star",
            features=pd.DataFrame({"feature": ["x"]}),
        ),
        PoseSet(
            position=np.array([[1, 2, 3]]),
            shift=np.array([[0.01, 0.02, 0.03]]),
            orientation=_rotations[1:],
            experiment_id="b",
            pixel_spacing=10,
            source="test.star",
            features=pd.DataFrame({"feature": ["y"]}),
        ),
    )


@pytest.fixture
def poseset2D():
    return (
        PoseSet(
            position=np.array([[1, 2, 0]]),
            shift=np.array([[0.01, 0.02, 0]]),
            orientation=Rotation.from_euler("Z", [60], degrees=True).inv(),
            experiment_id="a",
            pixel_spacing=10,
            source="test.star",
        ),
        PoseSet(
            position=np.array([[1, 2, 0]]),
            shift=np.array([[0.01, 0.02, 0]]),
            orientation=Rotation.from_euler("Z", [45], degrees=True).inv(),
            experiment_id="b",
            pixel_spacing=10,
            source="test.star",
        ),
    )


@pytest.fixture
def relion30_star():
    return pd.DataFrame(
        {
            "rlnCoordinateX": [1, 1],
            "rlnCoordinateY": [2, 2],
            "rlnCoordinateZ": [3, 3],
            "rlnOriginX": [-0.01, -0.01],
            "rlnOriginY": [-0.02, -0.02],
            "rlnOriginZ": [-0.03, -0.03],
            "rlnAngleRot": _angles_relion[:, 0],
            "rlnAngleTilt": _angles_relion[:, 1],
            "rlnAnglePsi": _angles_relion[:, 2],
            "rlnMicrographName": ["a", "b"],
            "rlnDetectorPixelSize": [10, 10],
            "feature": ["x", "y"],
        }
    )


@pytest.fixture
def relion31_star():
    df_optics = pd.DataFrame(
        {
            "rlnOpticsGroup": [1],
            "rlnImagePixelSize": [10],
        }
    )
    df_particles = pd.DataFrame(
        {
            "rlnCoordinateX": [1, 1],
            "rlnCoordinateY": [2, 2],
            "rlnCoordinateZ": [3, 3],
            "rlnOriginXAngst": [-0.1, -0.1],
            "rlnOriginYAngst": [-0.2, -0.2],
            "rlnOriginZAngst": [-0.3, -0.3],
            "rlnAngleRot": _angles_relion[:, 0],
            "rlnAngleTilt": _angles_relion[:, 1],
            "rlnAnglePsi": _angles_relion[:, 2],
            "rlnMicrographName": ["a", "b"],
            "feature": ["x", "y"],
            "rlnOpticsGroup": [1, 1],
        }
    )
    return {"optics": df_optics, "particles": df_particles}


@pytest.fixture
def relion40_star():
    df_optics = pd.DataFrame(
        {
            "rlnOpticsGroup": [1],
            "rlnTomoTiltSeriesPixelSize": [10],
        }
    )
    df_particles = pd.DataFrame(
        {
            "rlnCoordinateX": [1, 1],
            "rlnCoordinateY": [2, 2],
            "rlnCoordinateZ": [3, 3],
            "rlnOriginXAngst": [-0.1, -0.1],
            "rlnOriginYAngst": [-0.2, -0.2],
            "rlnOriginZAngst": [-0.3, -0.3],
            "rlnAngleRot": _angles_relion[:, 0],
            "rlnAngleTilt": _angles_relion[:, 1],
            "rlnAnglePsi": _angles_relion[:, 2],
            "rlnTomoName": ["a", "b"],
            "feature": ["x", "y"],
            "rlnOpticsGroup": [1, 1],
        }
    )
    return {"optics": df_optics, "particles": df_particles}


@pytest.fixture
def relion40_star2D():
    df_optics = pd.DataFrame(
        {
            "rlnOpticsGroup": [1],
            "rlnTomoTiltSeriesPixelSize": [10],
        }
    )
    df_particles = pd.DataFrame(
        {
            "rlnCoordinateX": [1, 1],
            "rlnCoordinateY": [2, 2],
            "rlnOriginXAngst": [-0.1, -0.1],
            "rlnOriginYAngst": [-0.2, -0.2],
            "rlnAnglePsi": [60, 45],
            "rlnTomoName": ["a", "b"],
            "feature": ["x", "y"],
            "rlnOpticsGroup": [1, 1],
        }
    )
    return {"optics": df_optics, "particles": df_particles}


@pytest.fixture
def dynamo_tbl():
    return pd.DataFrame(
        {
            "x": [1, 1],
            "y": [2, 2],
            "z": [3, 3],
            "dx": [0.01, 0.01],
            "dy": [0.02, 0.02],
            "dz": [0.03, 0.03],
            "tdrot": _angles_dynamo[:, 0],
            "tilt": _angles_dynamo[:, 1],
            "narot": _angles_dynamo[:, 2],
            "tomo": [0, 1],
            "feature": ["x", "y"],
        }
    )


@pytest.fixture
def image_stack():
    return Image(
        data=np.ones((3, 3, 3), dtype=np.float32),
        experiment_id="test",
        pixel_spacing=1,
        source="",
        stack=True,
    )


@pytest.fixture
def volume():
    return Image(
        data=np.ones((3, 3, 3), dtype=np.float32),
        experiment_id="test",
        pixel_spacing=1,
        source="",
        stack=False,
    )
