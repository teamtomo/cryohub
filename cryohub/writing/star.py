from pathlib import Path

import numpy as np
import pandas as pd
import starfile

from ..utils.constants import Relion
from ..utils.generic import listify
from ..utils.star import extract_optics


def write_star(particles, file_path, version="4.0", overwrite=False):
    """
    write particle data to disk as a .star file
    """
    particles = listify(particles)
    file_path = Path(file_path)

    dataframes = []
    for poseset in particles:
        df = pd.DataFrame()
        if np.allclose(poseset.position[:, 2], 0):
            # 2D data
            df[Relion.COORD_HEADERS[:2]] = poseset.position[:, :2]
        else:
            df[Relion.COORD_HEADERS] = poseset.position

        px_size = poseset.pixel_spacing
        df[Relion.PIXEL_SIZE_HEADER[version]] = px_size

        shift = poseset.shift
        if shift is not None:
            if version != "3.0":
                # shifts are in Angstroms (we need to go to numpy and resize or indices mess up stuff)
                shift = shift * px_size

            # shifts are subtractive in relion
            shift = -shift

            if np.allclose(shift[:, 2], 0):
                # 2D data
                df[Relion.SHIFT_HEADERS[version][:2]] = shift[:, :2]
            else:
                df[Relion.SHIFT_HEADERS[version]] = shift

        # invert rotations for relion and convert to euler (in degrees)
        ori = poseset.orientation
        if ori is not None:
            rotvec = ori.inv().as_rotvec(degrees=True)
            if np.allclose(rotvec[:, :2], 0):
                # single angle world
                df[Relion.EULER_HEADERS[2]] = rotvec[:, 2]
            else:
                df[Relion.EULER_HEADERS] = ori.inv().as_euler(
                    Relion.EULER, degrees=True
                )

        # useful to keep around
        df["experiment_id"] = poseset.experiment_id

        if poseset.features is not None:
            df = pd.concat([df, poseset.features.reset_index(drop=True)], axis=1)

        dataframes.append(df)

    df = pd.concat(dataframes)

    # split out optics group if present (and version > 3.0)
    if version != "3.0":
        data = extract_optics(df)
    else:
        data = df

    if not file_path.suffix:
        file_path = file_path.with_suffix(".star")

    starfile.write(data, file_path, overwrite=overwrite)
