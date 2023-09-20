import mrcfile
import numpy as np
import starfile

from cryohub.utils.testing import assert_dataframe_equal
from cryohub.writing.main import write


def test_write_path(tmp_path, image_stack, volume, poseset, relion40_star):
    mrc_path1 = tmp_path / "test1.mrc"
    mrc_path2 = tmp_path / "test2.mrc"
    star_path = tmp_path / "test.star"

    write(image_stack, mrc_path1)
    write(volume, mrc_path2)
    write(poseset, star_path)

    np.testing.assert_array_equal(mrcfile.open(mrc_path1).data, image_stack.data)
    np.testing.assert_array_equal(mrcfile.open(mrc_path2).data, volume.data)
    for df1, df2 in zip(
        starfile.read(star_path, always_dict=True).values(), relion40_star.values()
    ):
        assert_dataframe_equal(df1, df2)
