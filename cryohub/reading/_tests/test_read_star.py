import starfile

from cryohub.reading.star import read_star
from cryohub.utils.testing import assert_dataclass_equal


def test_read_relion30_3d(tmp_path, relion30_star, poseset):
    file_path = tmp_path / "test.star"
    starfile.write(relion30_star, file_path)

    part = read_star(file_path, name_regex=r"\w")

    for p, p_exp in zip(part, poseset):
        assert_dataclass_equal(p, p_exp)


def test_read_relion31_3d(tmp_path, relion31_star, poseset):
    file_path = tmp_path / "test.star"
    starfile.write(relion31_star, file_path)

    part = read_star(file_path, name_regex=r"\w")

    for p, p_exp in zip(part, poseset):
        assert_dataclass_equal(p, p_exp)


def test_read_relion40_3d(tmp_path, relion40_star, poseset):
    file_path = tmp_path / "test.star"
    starfile.write(relion40_star, file_path)

    part = read_star(file_path, name_regex=r"\w")

    for p, p_exp in zip(part, poseset):
        assert_dataclass_equal(p, p_exp)


def test_read_relion40_2d(tmp_path, relion40_star2D, poseset2D):
    file_path = tmp_path / "test.star"
    starfile.write(relion40_star2D, file_path)

    part = read_star(file_path, name_regex=r"\w")

    for p, p_exp in zip(part, poseset2D):
        assert_dataclass_equal(p, p_exp)
