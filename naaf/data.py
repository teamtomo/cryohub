from pathlib import Path
from typing import Optional, Union

import dask.array as da
import numpy as np
import pandas as pd
from pydantic import BaseModel, validator


class Data(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    name: Optional[str] = None
    source: Optional[Path] = None
    pixel_size: Optional[float] = None

    @validator("pixel_size")
    def _validate_pixel_size(cls, v):
        if v is not None:
            # TODO: for now just make everything 3D
            return np.broadcast_to(v, (3,))


class Particles(Data):
    data: pd.DataFrame


class Image(Data):
    data: Union[np.ndarray, da.Array]
