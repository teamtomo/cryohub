import dynamotable
from cryotypes.poseset import PoseSetDataLabels as PSDL

from naaf.reading.tbl import read_tbl
from naaf.utils.testing import assert_dataframe_equal

base_columns = [
    *PSDL.POSITION,
    *PSDL.SHIFT,
    PSDL.ORIENTATION,
]


def test_read_tbl(tmp_path, dynamo_tbl, poseset):
    file_path = tmp_path / "test.tbl"
    dynamotable.write(dynamo_tbl, file_path)

    part = read_tbl(file_path, name_regex=r"\w")

    assert_dataframe_equal(part, poseset, columns=base_columns)
