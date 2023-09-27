from pathlib import Path

from ..utils.generic import ParseError, listify
from .box import read_box
from .cbox import read_cbox
from .em import read_em
from .eman2_hdf import read_eman2_hdf
from .eman2_json import read_eman2_json
from .mrc import read_mrc
from .star import read_star
from .tbl import read_tbl
from .tif import read_tif

# a mapping of file extensions to readers, tuple map to tuples (don't forget trailing comma!):
#   - multiple extensions values in the keys use the same readers
#   - multiple readers are called in order from highest to lowers in case previous ones fail
# TODO: put this directly in the readers to make it plug and play?
readers = {
    (".box",): (read_box,),
    (".cbox",): (read_cbox,),
    (".em",): (read_em,),
    (".hdf",): (read_eman2_hdf,),
    (".json",): (read_eman2_json,),
    (".mrc", ".mrcs", ".st", ".map"): (read_mrc,),
    (".star",): (read_star,),
    (".tbl",): (read_tbl,),
    (".tif", ".tiff"): (read_tif,),
}

known_formats = [ext for formats in readers for ext in formats]


def read_file(file_path, **kwargs):
    """
    read a single file with the appropriate parser and return a list
    """
    for ext, funcs in readers.items():
        if file_path.suffix in ext:
            for func in funcs:
                try:
                    data = listify(func(file_path, **kwargs))
                    for d in data:
                        d.source = file_path
                    return data
                except ParseError:
                    # this will be raised by individual readers when the file can't be read.
                    # Keep trying until all options are exhausted
                    continue
    raise ParseError(f"could not read {file_path}")


def filter_readable(paths):
    for path in paths:
        path = Path(path)
        if path.is_dir():
            yield from filter_readable(path.iterdir())
        if path.is_file() and path.suffix in known_formats:
            yield path


def read(
    *paths,
    guess_id=True,
    name_regex=None,
    names=None,
    strict=False,
    lazy=True,
    **kwargs,
):
    r"""
    Read any number of paths.

    guess_id:   try to guess experiment ids from the raw data, using default regexes
                ("\w+_\d+" and "\d+") or a custom one provided with name_regex
    name_regex: a regex used to infer names from paths or micrograph names. For example:
                'Protein_\d+' will match 'MyProtein_10.star' and 'MyProtein_001.mrc'
                and name the respective DataBlocks 'Protein_10' and 'Protein_01'
    names:      a list of strings: anything whose name is not in this list will be discarded.
    strict:     if set to true, immediately fail if a matched filename cannot be read
    lazy:       read data lazily (if possible)
    """
    data = []
    for file in filter_readable(paths):
        try:
            data.extend(
                read_file(
                    file, name_regex=name_regex, guess_id=guess_id, lazy=lazy, **kwargs
                )
            )
        except ParseError:
            if strict:
                raise
    if not data and strict:
        raise ParseError(f"could not read any data from {paths}")

    if names is not None:
        data = [d for d in data if d.name in names]
    return data
