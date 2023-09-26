import dask.array as da
import emfile
import numpy as np
from cryotypes.image import Image, validate_image

from ..utils.generic import guess_name


def read_em(image_path, name_regex=None, lazy=True, **kwargs):
    """
    read an em image file
    """
    name = guess_name(image_path, name_regex)

    header, data = emfile.read(image_path, mmap=True)

    if lazy:
        data = da.from_array(data)
    else:
        data = np.asarray(data)

    pixel_size = header["OBJ"] or 0

    img = Image(
        data=data,
        experiment_id=name,
        pixel_spacing=pixel_size,
        source=image_path,
        stack=False,
    )

    return validate_image(img, coerce=True)
