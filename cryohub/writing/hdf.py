import h5py


def write_hdf(image, file_path, overwrite=False):
    """
    write an image to disk as an .hdf file
    """
    if not file_path.endswith(".hdf"):
        file_path = file_path + ".hdf"

    mode = "w" if overwrite else "x"

    with h5py.File(file_path, mode=mode) as hdf:
        # TODO: how does this vary?
        (
            hdf.create_group("MDF")
            .create_group("images")
            .create_group("0")
            .create_dataset("image", data=image.data)
        )
