import emfile

from cryohub.reading.em import read_em
from cryohub.utils.testing import assert_dataclass_equal

base_fields = ["data", "experiment_id", "pixel_spacing", "stack"]


def test_read_em(tmp_path, volume):
    file_path = tmp_path / "test.em"
    emfile.write(str(file_path), volume.data)
    em = read_em(file_path, name_regex=r"\w+", lazy=False)

    assert_dataclass_equal(em, volume, fields=base_fields)
