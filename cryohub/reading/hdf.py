import h5py
import numpy as np
from cryotypes.image import Image, validate_image

from ..utils.generic import guess_name


# TODO: lazy mode
def read_hdf(image_path, name_regex=None, **kwargs):
    """
    read an hdf file
    """
    name = guess_name(image_path, name_regex)

    with h5py.File(image_path, mode="r") as hdf:
        # TODO: how does this vary?
        img = hdf["MDF"]["images"]["0"]["image"]
        data = np.asarray(img)

    tomo = Image(
        data=data,
        experiment_id=name,
        pixel_spacing=None or 0,
        source=image_path,
        stack=False,
    )

    return validate_image(tomo, coerce=True)
