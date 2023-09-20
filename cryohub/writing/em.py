from pathlib import Path

import emfile

from ..utils.generic import WriteError, listify


def write_em(image, file_path, overwrite=False):
    """
    write an image to disk as an .em file
    """
    image = listify(image)
    file_path = Path(file_path)
    if len(image) != 1:
        raise WriteError("Cannot write multiple images to the same path.")
    image = image[0]

    if not file_path.suffix:
        file_path = file_path.with_suffix(".em")

    # TODO: pass pixel size and other stuff to header
    emfile.write(file_path, image.data, header_params={}, overwrite=overwrite)
