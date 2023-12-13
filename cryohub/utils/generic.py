import re
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
from cryotypes.image import ImageProtocol
from cryotypes.poseset import PoseSetProtocol


class ParseError(RuntimeError):
    pass


class WriteError(RuntimeError):
    pass


# a list of commonly used base names for paths in regex form
common_name_regexes = (
    r"^(\w+\d+).*\.",
    r"^(\w+_\d+).*\.",
    r"^(.*\d+).*\.",
    r"^(.*?)\.",
    r"^\w+",
)


def guess_name(string, name_regex=None):
    """
    guess an appropriate name based on the input string
    and a list of regexes in order of priority
    """
    if string is None:
        return "NO_ID"
    string = Path(str(string)).stem
    name_regex = listify(name_regex)
    regexes = list(common_name_regexes)
    regexes = name_regex + regexes
    for regex in regexes:
        if match := re.search(regex, str(string)):
            if match.groups():
                return match.group(1)
            return match.group(0)
    else:
        return "NO_ID"


def pad_to_3D(arr):
    if arr.shape[-1] == 2:
        arr = np.pad(arr, ((0, 0), (0, 1)))
    return arr


def listify(obj):
    """
    transform input into an appropriate list, unless already list-like
    """
    if isinstance(obj, Iterable):
        if isinstance(obj, (str, Path, PoseSetProtocol, ImageProtocol)):
            return [obj]
        else:
            return list(obj)
    if obj is None:
        return []
    return [obj]


def get_columns_or_default(df, columns, default=0):
    """
    Get columns from a dataframe as a numpy array, if present.

    If only some columns are present, fill them with the default value.
    If none are present, return None.
    """
    if columns is None:
        return None
    if isinstance(columns, str):
        columns = [columns]

    cols = {}
    for col in columns:
        cols[col] = df.get(col, default)

    if not any(isinstance(col, pd.Series) for col in cols.values()):
        return None

    return np.asarray(pd.DataFrame(cols, index=df.index))
