from pathlib import Path

from pydantic import BaseModel
import numpy as np
import pandas as pd
import dask.array as da
from scipy.spatial.transform import Rotation


class Data(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    name: str | None = None
    source: Path | None = None
    pixel_size: float | None = None

    def __eq__(self, other):
        if not isinstance(other, BaseModel):
            return self.dict() == other
        s = self.dict()
        o = other.dict()
        for f, v in s.items():
            if f not in o:
                return False
            elif isinstance(v, (np.ndarray, da.Array)):
                try:
                    if not np.allclose(v, o[f]):
                        return False
                except TypeError:
                    if not np.all(v == o[f]):
                        return False
            elif isinstance(v, pd.DataFrame):
                for col in v:
                    if col not in v:
                        return False
                    try:
                        if not np.allclose(v[col], o[f][col]):
                            return False
                    except TypeError:
                        if not np.all(v[col] == o[f][col]):
                            return False
            elif isinstance(v, Rotation):
                back_forth = (v.inv() * o[f]).reduce().as_rotvec()
                if not np.allclose(back_forth, 0):
                    return False
            else:
                if not v == o[f]:
                    return False
        return True


class Particles(Data):
    coords: np.ndarray | da.Array
    rot: Rotation
    features: pd.DataFrame | None = None


class Image(Data):
    data: np.ndarray | da.Array
