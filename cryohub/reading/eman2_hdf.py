import h5py
import numpy as np
from cryotypes.image import Image, validate_image

from ..utils.generic import guess_name


def read_eman2_hdf(image_path, name_regex=None, **kwargs):
    """
    read an EMAN2 hdf file
    """
    name = guess_name(image_path, name_regex)

    with h5py.File(image_path, mode="r") as hdf:
        # TODO: how does this vary?
        img = hdf["MDF"]["images"]["0"]
        data = np.asarray(img["image"])

        px_size = img.attrs["EMAN.apix_x"].item()

    img = Image(
        data=data,
        experiment_id=name,
        pixel_spacing=px_size,
        source=image_path,
        stack=False,
    )

    return validate_image(img, coerce=True)
