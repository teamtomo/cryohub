import emfile


def write_em(image, file_path, overwrite=False):
    """
    write an image to disk as an .em file
    """
    if not file_path.endswith('.em'):
        file_path = file_path + '.em'
    # TODO: pass pixel size and other stuff to header
    emfile.write(file_path, image.data, header_params={}, overwrite=overwrite)
