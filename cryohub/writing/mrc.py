import mrcfile
import numpy as np


def _ensure_valid_dtype(data):
    dtype = np.dtype(data.dtype)
    if np.issubdtype(dtype, np.integer):
        # int can only go up to 16bit
        size = min(dtype.itemsize, 2)
        kind = dtype.kind
    elif np.issubdtype(dtype, np.floating):
        # float can only go up to 32bit
        size = min(dtype.itemsize, 4)
        kind = dtype.kind
    else:
        raise TypeError(f'cannot write mrc with dtype "{dtype}"')

    new_dtype = np.dtype(f"{kind}{size}")
    return np.array(data, dtype=new_dtype)


def write_mrc(image, file_path, overwrite=False):
    """
    write an image to disk as an .mrc file
    """
    if not file_path.endswith(".mrc"):
        file_path = file_path + ".mrc"

    mrc = mrcfile.new(file_path, _ensure_valid_dtype(image.data), overwrite=overwrite)
    mrc.set_image_stack() if image.stack else mrc.set_volume()
    mrc.voxel_size = image.pixel_spacing
    mrc.close()
