from pathlib import Path

from .star import read_star
from .mrc import read_mrc
from .em import read_em
from .tbl import read_tbl
from .box import read_box
from .cbox import read_cbox

from ..utils.generic import listify, ParseError

# a mapping of file extensions to readers, tuple map to tuples (don't forget trailing comma!):
#   - multiple extensions values in the keys use the same readers
#   - multiple readers are called in order from highest to lowers in case previous ones fail
# TODO: put this directly in the readers to make it plug and play?
readers = {
    ('.star',): (read_star,),
    ('.mrc', '.mrcs', '.map'): (read_mrc,),
    ('.em',): (read_em,),
    ('.tbl',): (read_tbl,),
    ('.box',): (read_box,),
    ('.cbox',): (read_cbox,),
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
                        # last item is metadata dictionary
                        d[-1]['source'] = file_path
                    return data
                except ParseError:
                    # this will be raised by individual readers when the file can't be read.
                    # Keep trying until all options are exhausted
                    continue
    raise ParseError(f'could not read {file_path}')


def root_relative_glob(glob):
    return str(Path(glob).expanduser().resolve().relative_to('/'))


def expand_globs(globs):
    """
    expand globs to single files
    """
    globs = listify(globs)
    for glob in globs:
        glob = root_relative_glob(glob)
        yield from Path('/').glob(glob)


def filter_readable(paths):
    for path in paths:
        if path.is_file() and path.suffix in known_formats:
            yield path


def find_files(globs):
    """
    take a glob pattern or iterable thereof and find all readable files that match it
    """
    files = expand_globs(globs)
    readable = filter_readable(files)

    yield from readable


def read(
     *globs,
     name_regex=None,
     strict=False,
     lazy=True,
     **kwargs,
):
    r"""
    Read any number of paths or glob patterns.

    name_regex: a regex used to infer names from paths or micrograph names. For example:
                'Protein_\d+' will match 'MyProtein_10.star' and 'MyProtein_001.mrc'
                and name the respective DataBlocks 'Protein_10' and 'Protein_01'
    strict:     if set to true, immediately fail if a matched filename cannot be read
    lazy:       read data lazily (if possible)
    """
    data = []
    for file in find_files(globs):
        try:
            data.extend(read_file(file, name_regex=name_regex, lazy=lazy, **kwargs))
        except ParseError:
            if strict:
                raise
    if not data and strict:
        raise ParseError(f'could not read any data from {globs}')

    return data
