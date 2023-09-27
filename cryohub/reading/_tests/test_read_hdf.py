import h5py

from cryohub.reading.eman2_hdf import read_eman2_hdf
from cryohub.utils.testing import assert_dataclass_equal

base_fields = ["data", "experiment_id", "pixel_spacing", "stack"]


def test_read_hdf(tmp_path, volume):
    file_path = tmp_path / "test.hdf"

    with h5py.File(file_path, mode="w") as hdf:
        # TODO: how does this vary?
        (
            hdf.create_group("MDF")
            .create_group("images")
            .create_group("0")
            .create_dataset("image", data=volume.data)
        )

        hdf["MDF"]["images"]["0"].attrs["EMAN.apix_x"] = 1

    hdf = read_eman2_hdf(file_path, name_regex=r"\w+")

    assert_dataclass_equal(hdf, volume, fields=base_fields)
