import numpy as np
import mrcfile

from naaf.reading.mrc import read_mrc
from naaf.data import Image
from naaf.utils.testing import assert_data_equal


def test_read_mrc(tmp_path):
    file_path = tmp_path / 'test.mrc'
    data = np.ones((3, 3, 3), dtype=np.float32)
    mrcfile.new(str(file_path), data)
    image = read_mrc(file_path, name_regex=r'\w+', lazy=False)

    expected = Image(
        data=data,
        name='test',
    )

    assert_data_equal(image, expected)
