import dask.array as da
import mrcfile
import numpy as np
from numpy.lib.recfunctions import structured_to_unstructured

from ..data import Image
from ..utils.generic import guess_name


def read_mrc(image_path, name_regex=None, lazy=True, **kwargs):
    """
    read an mrc file
    """
    name = guess_name(image_path, name_regex)

    with mrcfile.mmap(image_path) as mrc:
        if lazy:
            data = da.from_array(mrc.data)
        else:
            data = np.asarray(mrc.data)

        # TODO: support anisotropic pixel sizes
        pixel_size = structured_to_unstructured(mrc.voxel_size)[0] or None

        stack = mrc.is_image_stack() or mrc.is_volume_stack()

    return Image(
        data=data,
        name=name,
        pixel_size=pixel_size,
        stack=stack,
    )
