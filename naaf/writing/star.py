import numpy as np
import pandas as pd
import starfile
from cryotypes.poseset import PoseSetDataLabels as PSDL
from scipy.spatial.transform import Rotation

from ..utils.constants import POSESET_REDUNDANT_HEADERS, Relion


def write_star(particles, file_path, version="4.0", overwrite=False):
    """
    write particle data to disk as a .star file
    """
    ndim = 3 if PSDL.POSITION_Z in particles.columns else 2

    df = pd.DataFrame()
    df[Relion.COORD_HEADERS[:ndim]] = particles[PSDL.POSITION[:ndim]]

    px_size = particles[PSDL.PIXEL_SPACING]
    shifts = particles[PSDL.SHIFT[:ndim]]
    if version != "3.0":
        # shifts are in Angstroms (we need to go to numpy and resize or indices mess up stuff)
        shifts *= px_size.to_numpy().reshape(len(px_size), -1)
    df[Relion.PIXEL_SIZE_HEADER[version]] = px_size
    df[
        Relion.SHIFT_HEADERS[version][:ndim]
    ] = -shifts  # shifts are subtractive in relion

    rot = Rotation.concatenate(particles[PSDL.ORIENTATION]).inv()
    eulers = rot.as_euler(Relion.EULER, degrees=True)  # invert for relion
    if np.allclose(eulers[:, 1:], 0):
        # single angle world
        df[Relion.EULER_HEADERS[2]] = eulers[:, 0]
    else:
        df[Relion.EULER_HEADERS] = eulers
    df[Relion.MICROGRAPH_NAME_HEADER[version]] = particles[PSDL.EXPERIMENT_ID]

    features = particles.drop(columns=POSESET_REDUNDANT_HEADERS, errors="ignore")
    df = pd.concat([df, features], axis=1)

    # split out optics group if present
    if Relion.OPTICS_GROUP_HEADER in particles.columns:
        optics_headers = [
            h for h in Relion.POSSIBLE_OPTICS_GROUP_HEADERS if h in particles.columns
        ]
        optics = (
            df.get([Relion.OPTICS_GROUP_HEADER] + optics_headers)
            .drop_duplicates()
            .reset_index(drop=True)
        )
        particles = df.drop(columns=optics_headers, errors="ignore")
        data = {"optics": optics, "particles": particles}
    else:
        data = df

    if not str(file_path).endswith(".star"):
        file_path = str(file_path) + ".star"

    starfile.write(data, file_path, overwrite=overwrite)
