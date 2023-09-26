import dask.array as da
import mrcfile
import numpy as np
from cryotypes.image import Image, validate_image
from numpy.lib.recfunctions import structured_to_unstructured

from ..utils.generic import guess_name


def read_mrc(image_path, name_regex=None, lazy=True, **kwargs):
    """
    read an mrc file
    """
    name = guess_name(image_path, name_regex)

    with mrcfile.mmap(image_path, "r", permissive=True) as mrc:
        if lazy:
            data = da.from_array(mrc.data)
        else:
            data = np.asarray(mrc.data)

        # TODO: support anisotropic pixel sizes
        pixel_size = structured_to_unstructured(mrc.voxel_size)[0] or 0

        stack = mrc.is_image_stack() or mrc.is_volume_stack()

    img = Image(
        data=data,
        experiment_id=name,
        pixel_spacing=pixel_size,
        source=image_path,
        stack=stack,
    )

    return validate_image(img, coerce=True)
