import mrcfile

from cryohub.reading.mrc import read_mrc
from cryohub.utils.testing import assert_dataclass_equal

base_fields = ["data", "experiment_id", "pixel_spacing", "stack"]


def test_read_mrc_stack(tmp_path, image_stack):
    file_path = tmp_path / "test.mrc"
    mrcfile.new(str(file_path), image_stack.data)
    mrc = read_mrc(file_path, name_regex=r"\w+", lazy=False)

    assert_dataclass_equal(mrc, image_stack, fields=base_fields)


def test_read_mrc_volume(tmp_path, volume):
    file_path = tmp_path / "test.mrc"
    mrcfile.new(str(file_path), volume.data)
    mrc = read_mrc(file_path, name_regex=r"\w+", lazy=False)

    assert_dataclass_equal(mrc, volume, fields=base_fields)
