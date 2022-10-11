import emfile

from cryohub.writing.em import write_em


def test_write_em(tmp_path, volume):
    file_path = tmp_path / "test.em"
    write_em(volume, str(file_path))
    _, data = emfile.read(file_path)
    assert data.shape == (3, 3, 3)
