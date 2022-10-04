import mrcfile


def write_mrc(image, file_path, overwrite=False):
    """
    write an image to disk as an .mrc file
    """
    if not file_path.endswith(".mrc"):
        file_path = file_path + ".mrc"

    mrc = mrcfile.new(file_path, image.data, overwrite=overwrite)
    mrc.set_image_stack() if image.stack else mrc.set_volume()
    mrc.voxel_size = image.pixel_spacing
    mrc.close()
