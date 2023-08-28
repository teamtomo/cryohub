from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from numpy.typing import ArrayLike
from scipy.spatial.transform import Rotation


@dataclass
class PoseSet:
    position: ArrayLike
    experiment_id: str
    source: Path | str
    pixel_spacing: float = 0
    shift: ArrayLike | None = None
    orientation: Rotation | None = None
    features: pd.DataFrame | None = None
