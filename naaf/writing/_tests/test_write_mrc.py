import numpy as np

from naaf.writing.mrc import write_mrc
from naaf.data import Image


def test_write_mrc(tmp_path):
    file_path = tmp_path / 'test.mrc'
    imageblock = Image(data=np.ones((3, 3, 3), dtype=np.float32))
    write_mrc(imageblock, str(file_path))
