import re
from pathlib import Path
from typing import Iterable

from ..data import Data


class ParseError(RuntimeError):
    pass


# a list of commonly used base names for paths in regex form
common_name_regexes = (
    r"TS_\d+",
    r"series_\d+",
    r"_\d+",
    r"\d+",
)


def guess_name(string, name_regex=None):
    """
    guess an appropriate name based on the input string
    and a list of regexes in order of priority
    """
    if isinstance(string, Path):
        string = string.stem
    name_regex = listify(name_regex)
    regexes = list(common_name_regexes)
    regexes = name_regex + regexes
    for regex in regexes:
        if match := re.search(regex, str(string)):
            return match.group(0)
    else:
        return None


def listify(obj):
    """
    transform input into an appropriate list, unless already list-like
    """
    if isinstance(obj, Iterable):
        if isinstance(obj, (str, Path, Data)):
            return [obj]
        else:
            return list(obj)
    if obj is None:
        return []
    return [obj]
