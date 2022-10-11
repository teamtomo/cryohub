import re
from pathlib import Path
from typing import Iterable

import numpy as np
from cryotypes.image import ImageProtocol
from cryotypes.poseset import PoseSet


class ParseError(RuntimeError):
    pass


# a list of commonly used base names for paths in regex form
common_name_regexes = (
    r"\w+_\d+",
    r"\d+",
)


def guess_name(string, name_regex=None):
    """
    guess an appropriate name based on the input string
    and a list of regexes in order of priority
    """
    if string is None:
        return ""
    if isinstance(string, Path):
        string = string.stem
    name_regex = listify(name_regex)
    regexes = list(common_name_regexes)
    regexes = name_regex + regexes
    for regex in regexes:
        if match := re.search(regex, str(string)):
            if match.groups():
                return match.group(1)
            return match.group(0)
    else:
        return ""


@np.vectorize
def guess_name_vec(string, reg=None):
    return guess_name(string, reg)


def pad_to_3D(arr):
    if arr.shape[-1] == 2:
        arr = np.pad(arr, ((0, 0), (0, 1)))
    return arr


def listify(obj):
    """
    transform input into an appropriate list, unless already list-like
    """
    if isinstance(obj, Iterable):
        if isinstance(obj, (str, Path, PoseSet, ImageProtocol)):
            return [obj]
        else:
            return list(obj)
    if obj is None:
        return []
    return [obj]
