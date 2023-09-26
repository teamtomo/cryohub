import dask.array as da
import tifffile
from cryotypes.image import Image, validate_image

from ..utils.generic import guess_name


def read_tif(image_path, name_regex=None, lazy=True, **kwargs):
    """
    read an tif file
    """
    name = guess_name(image_path, name_regex)

    with tifffile.TiffFile(image_path) as tif:
        if lazy:
            data = da.from_zarr(tif.aszarr())
        else:
            data = tif.asarray()
        pixel_size = (
            10000 / tif.pages.first.get_resolution(tifffile.RESUNIT.MICROMETER)[-1]
        )

    stack = data.ndim == 3

    img = Image(
        data=data,
        experiment_id=name,
        pixel_spacing=pixel_size,
        source=image_path,
        stack=stack,
    )

    return validate_image(img, coerce=True)
