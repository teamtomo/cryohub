import mrcfile


def write_mrc(image, file_path, overwrite=False):
    """
    write an image to disk as an .mrc file
    """
    if not file_path.endswith('.mrc'):
        file_path = file_path + '.mrc'
    # TODO: pass pixel size and other stuff to header
    mrcfile.new(file_path, image.data, overwrite=overwrite)
