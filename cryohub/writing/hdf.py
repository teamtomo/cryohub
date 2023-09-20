from pathlib import Path

import h5py

from ..utils.generic import WriteError, listify


def write_hdf(image, file_path, overwrite=False):
    """
    write an image to disk as an .hdf file
    """
    image = listify(image)
    file_path = Path(file_path)
    if len(image) != 1:
        raise WriteError("Cannot write multiple images to the same path.")
    image = image[0]

    if not file_path.suffix:
        file_path = file_path.with_suffix(".hdf")

    mode = "w" if overwrite else "x"

    with h5py.File(file_path, mode=mode) as hdf:
        # TODO: how does this vary?
        (
            hdf.create_group("MDF")
            .create_group("images")
            .create_group("0")
            .create_dataset("image", data=image.data)
        )
