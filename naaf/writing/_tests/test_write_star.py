import pandas as pd
import starfile

from naaf.utils.constants import Relion
from naaf.utils.testing import assert_dataframe_equal
from naaf.writing.star import write_star

version = "4.0"

base_columns = [
    *Relion.COORD_HEADERS,
    *Relion.SHIFT_HEADERS[version],
    *Relion.EULER_HEADERS,
    Relion.PIXEL_SIZE_HEADER[version],
    Relion.MICROGRAPH_NAME_HEADER[version],
]


def test_write_star3D(tmp_path, poseset, relion40_star):
    file_path = tmp_path / "test.star"

    write_star(poseset, file_path)
    data = starfile.read(file_path)
    expected = pd.merge(
        relion40_star["particles"], relion40_star["optics"], on="rlnOpticsGroup"
    )
    assert_dataframe_equal(data, expected, columns=base_columns + ["feature"])


def test_write_star2D(tmp_path, poseset2D, relion40_star2D):
    file_path = tmp_path / "test.star"

    write_star(poseset2D, file_path)
    data = starfile.read(file_path)
    expected = pd.merge(
        relion40_star2D["particles"], relion40_star2D["optics"], on="rlnOpticsGroup"
    )
    assert_dataframe_equal(data, expected, columns=base_columns)
