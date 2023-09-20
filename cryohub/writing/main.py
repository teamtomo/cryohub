from pathlib import Path

from cryotypes.image import ImageProtocol
from cryotypes.poseset import PoseSetProtocol

from ..utils.generic import WriteError, listify
from .em import write_em
from .hdf import write_hdf
from .mrc import write_mrc
from .star import write_star
from .tbl import write_tbl

# a mapping of file extensions to writers, tuple map to tuples (don't forget trailing comma!):
#   - multiple extensions values in the keys use the same writers
#   - multiple writers are called in order from highest to lowers in case previous ones fail
#   - empty suffix must be in the last option (fallback)
# TODO: put this directly in the writers to make it plug and play?
writers_poses = {
    (".tbl",): (write_tbl,),
    (".star", ""): (write_star,),
}

writers_images = {
    (".hdf",): (write_hdf,),
    (".em",): (write_em,),
    (".mrc", ".mrcs", ".st", ".map", ""): (write_mrc,),
}


def write(data, file_path, **kwargs):
    """
    write a single file with the appropriate function
    """
    file_path = Path(file_path)
    data = listify(data)
    if all(isinstance(d, PoseSetProtocol) for d in data):
        writers = writers_poses
    elif all(isinstance(d, ImageProtocol) for d in data):
        writers = writers_images
    else:
        raise WriteError(f"No writer available for object of type {data[0].__class__}")

    for ext, funcs in writers.items():
        if file_path.suffix in ext:
            for func in funcs:
                try:
                    func(data, file_path, **kwargs)
                    return
                except WriteError:
                    # this will be raised by individual writers when the file can't be written.
                    # Keep trying until all options are exhausted
                    continue
    raise WriteError(f"could not write {file_path}")
