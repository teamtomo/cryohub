from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel
import numpy as np
import pandas as pd
import dask.array as da
from scipy.spatial.transform import Rotation


class Data(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    name: Optional[str] = None
    source: Optional[Path] = None
    pixel_size: Optional[float] = None

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
                    if isinstance(v[col][0], Rotation):
                        s_rot = Rotation.concatenate(v[col])
                        o_rot = Rotation.concatenate(o[f][col])
                        # invert and multiply should give zero
                        back_forth = (s_rot * o_rot.inv()).reduce().as_rotvec()
                        if not np.allclose(back_forth, 0):
                            return False
                    else:
                        try:
                            if not np.allclose(v[col], o[f][col]):
                                return False
                        except TypeError:
                            if not np.all(v[col] == o[f][col]):
                                return False
            else:
                if not v == o[f]:
                    return False
        return True


class Particles(Data):
    data: pd.DataFrame


class Image(Data):
    data: Union[np.ndarray, da.Array]
