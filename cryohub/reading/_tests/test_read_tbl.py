import dynamotable

from cryohub.reading.tbl import read_tbl
from cryohub.utils.testing import assert_dataclass_equal


def test_read_tbl(tmp_path, dynamo_tbl, poseset):
    file_path = tmp_path / "test.tbl"
    dynamotable.write(dynamo_tbl, file_path)

    part = read_tbl(file_path, name_regex=r"\w")

    for p, p_exp in zip(part, poseset):
        assert_dataclass_equal(p, p_exp)
