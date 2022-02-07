from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel
import numpy as np
import pandas as pd
import dask.array as da


class Data(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    name: Optional[str] = None
    source: Optional[Path] = None
    pixel_size: Optional[float] = None

class Particles(Data):
    data: pd.DataFrame


class Image(Data):
    data: Union[np.ndarray, da.Array]
