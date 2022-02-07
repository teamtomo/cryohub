import numpy as np
import emfile

from naaf.reading.em import read_em
from naaf.data import Image
from naaf.utils.testing import assert_data_equal


def test_read_em(tmp_path):
    file_path = tmp_path / 'test.em'
    data = np.ones((3, 3, 3))
    emfile.write(str(file_path), data)
    image = read_em(file_path, name_regex=r'\w+', lazy=False)
    
    expected = Image(
        data=data,
        name='test',
    )

    assert_data_equal(image, expected)
