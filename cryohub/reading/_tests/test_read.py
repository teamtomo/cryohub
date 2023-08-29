import mrcfile
import starfile

from cryohub.reading.main import read


def test_read_path(tmp_path, image_stack, volume, relion40_star):
    # mrc file
    mrc_path1 = tmp_path / "test1.mrc"
    mrc_path2 = tmp_path / "test2.mrc"
    mrcfile.new(str(mrc_path1), image_stack.data)
    mrcfile.new(str(mrc_path2), volume.data)

    star_path = tmp_path / "test.star"
    starfile.write(relion40_star, star_path)

    data = read(tmp_path, name_regex=r"test\d")

    assert len(data) == 4  # 2 imgs and 2 posesets
