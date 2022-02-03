import numpy as np
import pandas as pd
import dask.array as da
import emfile

from ..utils.generic import guess_name


def read_em(
    image_path,
    name_regex=None,
    lazy=True,
    **kwargs
):
    """
    read an em image file
    """
    name = guess_name(image_path, name_regex)

    header, data = emfile.read(image_path, mmap=True)

    if lazy:
        data = da.from_array(data)
    else:
        data = np.asarray(data)

    pixel_size = header['OBJ']

    return data, {'name': name, 'pixel_size': pixel_size}
