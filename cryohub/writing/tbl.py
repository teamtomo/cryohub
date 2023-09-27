from pathlib import Path

import dynamotable
import numpy as np
import pandas as pd

from ..utils.constants import Dynamo
from ..utils.generic import listify


def write_tbl(particles, file_path):
    """
    write particle data to disk as a dynamo .tbl file
    """
    particles = listify(particles)
    file_path = Path(file_path)

    dataframes = []
    for poseset in particles:
        df = pd.DataFrame()

        if np.allclose(poseset.position[:, 2], 0):
            # 2D data
            df[Dynamo.COORD_HEADERS[:2]] = poseset.position[:, :2]
        else:
            df[Dynamo.COORD_HEADERS] = poseset.position

        shift = poseset.shift
        if shift is not None:
            if np.allclose(shift[:, 2], 0):
                # 2D data
                df[Dynamo.SHIFT_HEADERS[:2]] = shift[:, :2]
            else:
                df[Dynamo.SHIFT_HEADERS] = shift

        # invert rotations for Dynamo and convert to euler (in degrees)
        ori = poseset.orientation
        if ori is not None:
            rotvec = ori.inv().as_rotvec(degrees=True)
            if np.allclose(rotvec[:, :2], 0):
                # single angle world
                df[Dynamo.EULER_HEADERS[2]] = rotvec[:, 2]
            else:
                df[Dynamo.EULER_HEADERS[3]] = ori.inv().as_euler(
                    Dynamo.EULER, degrees=True
                )

        # useful to keep around
        df["experiment_id"] = poseset.experiment_id

        # original exp_id source might be saved as features, let's put it back in.
        # dynamo cannot take arbitrary columns, so we're not giving all features
        if poseset.features is not None:
            if Dynamo.EXP_ID_HEADER in poseset.features.columns:
                df[Dynamo.EXP_ID_HEADER] = poseset.features[Dynamo.EXP_ID_HEADER]

        dataframes.append(df)

    df = pd.concat(dataframes)

    if not file_path.suffix:
        file_path = file_path.with_suffix(".tbl")
    dynamotable.write(df, file_path)
