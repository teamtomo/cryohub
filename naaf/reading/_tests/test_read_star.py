import starfile
from cryotypes.poseset import PoseSetDataLabels as PSDL

from naaf.reading.star import read_star
from naaf.utils.testing import assert_dataframe_equal

base_columns = [
    *PSDL.POSITION,
    *PSDL.SHIFT,
    PSDL.ORIENTATION,
    PSDL.EXPERIMENT_ID,
    PSDL.PIXEL_SPACING,
    "feature",
]


def test_read_relion30_3d(tmp_path, relion30_star, poseset):
    file_path = tmp_path / "test.star"
    starfile.write(relion30_star, file_path)

    part = read_star(file_path, name_regex=r"\w")

    assert_dataframe_equal(part, poseset, columns=base_columns)


def test_read_relion31_3d(tmp_path, relion31_star, poseset):
    file_path = tmp_path / "test.star"
    starfile.write(relion31_star, file_path)

    part = read_star(file_path, name_regex=r"\w")

    assert_dataframe_equal(part, poseset, columns=base_columns)


def test_read_relion40_3d(tmp_path, relion40_star, poseset):
    file_path = tmp_path / "test.star"
    starfile.write(relion40_star, file_path)

    part = read_star(file_path, name_regex=r"\w")

    assert_dataframe_equal(part, poseset, columns=base_columns)


def test_read_relion40_2d(tmp_path, relion40_star2D, poseset2D):
    file_path = tmp_path / "test.star"
    starfile.write(relion40_star2D, file_path)

    part = read_star(file_path, name_regex=r"\w")

    assert_dataframe_equal(
        part,
        poseset2D,
        columns=[
            *PSDL.POSITION[:2],
            *PSDL.SHIFT[:2],
            PSDL.ORIENTATION,
            PSDL.EXPERIMENT_ID,
            PSDL.PIXEL_SPACING,
        ],
    )
