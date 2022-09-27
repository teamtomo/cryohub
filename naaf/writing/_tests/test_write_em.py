import numpy as np

from naaf.data import Image
from naaf.writing.em import write_em


def test_write_em(tmp_path):
    file_path = tmp_path / "test.em"
    imageblock = Image(data=np.ones((3, 3, 3)))
    write_em(imageblock, str(file_path))
