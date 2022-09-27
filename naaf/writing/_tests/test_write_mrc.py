import mrcfile
import numpy as np

from naaf.data import Image
from naaf.writing.mrc import write_mrc


def test_write_mrc(tmp_path):
    file_path = tmp_path / "test.mrc"
    imageblock = Image(
        data=np.ones((3, 3, 12), dtype=np.float32), pixel_size=2, stack=True
    )
    write_mrc(imageblock, str(file_path))
    with mrcfile.mmap(str(file_path)) as mrc:
        assert mrc.data.shape == (3, 3, 12)
        assert mrc.voxel_size.item()[0] == 2
        assert mrc.is_image_stack()
