import dynamotable

from cryohub.utils.constants import Dynamo
from cryohub.utils.testing import assert_dataframe_equal
from cryohub.writing.tbl import write_tbl

base_columns = [
    *Dynamo.COORD_HEADERS,
    *Dynamo.SHIFT_HEADERS,
    *Dynamo.EULER_HEADERS[3],
    # Dynamo.EXP_ID_HEADER,  # TODO: this currently is lost because we can't write using tomo names
]


def test_write_tbl(tmp_path, poseset, dynamo_tbl):
    file_path = tmp_path / "test.tbl"

    write_tbl(poseset, file_path)
    data = dynamotable.read(file_path)
    assert_dataframe_equal(data, dynamo_tbl, columns=base_columns)
