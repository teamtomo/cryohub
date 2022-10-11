import mrcfile

from cryohub.writing.mrc import write_mrc


def test_write_mrc_stack(tmp_path, image_stack):
    file_path = tmp_path / "test.mrc"
    write_mrc(image_stack, str(file_path))
    with mrcfile.mmap(str(file_path)) as mrc:
        assert mrc.data.shape == (3, 3, 3)
        assert mrc.voxel_size.item()[0] == 1
        assert mrc.is_image_stack()


def test_write_mrc_volume(tmp_path, volume):
    file_path = tmp_path / "test.mrc"
    write_mrc(volume, str(file_path))
    with mrcfile.mmap(str(file_path)) as mrc:
        assert mrc.data.shape == (3, 3, 3)
        assert mrc.voxel_size.item()[0] == 1
        assert mrc.is_volume()
