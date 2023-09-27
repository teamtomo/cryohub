import json

import numpy as np
import pandas as pd
from cryotypes.poseset import validate_poseset

from ..utils.generic import guess_name
from ..utils.types import PoseSet


def read_eman2_json(
    json_path,
    name_regex=None,
    center_on_tomo=None,
    **kwargs,
):
    with open(json_path) as f:
        data = json.load(f)

    coords = np.array([el[:3] for el in data["boxes_3d"]], dtype=float)
    if not len(coords):
        coords = np.empty((0, 3), dtype=float)

    method = np.array([el[3] for el in data["boxes_3d"]], dtype=str)
    score = np.array([el[4] for el in data["boxes_3d"]], dtype=float)
    particle_class = np.array([el[5] for el in data["boxes_3d"]], dtype=int)

    features = pd.DataFrame({"method": method, "score": score, "class": particle_class})
    class_features = pd.DataFrame(
        {int(k): v for k, v in data["class_list"].items()}
    ).T.reset_index(names="class")

    features = pd.merge(features, class_features, on="class")

    name = guess_name(json_path, name_regex)
    px_size = data["apix_unbin"]

    if center_on_tomo is not None:
        import h5py

        with h5py.File(center_on_tomo, mode="r") as hdf:
            img = hdf["MDF"]["images"]["0"]
            shape = np.array(img["image"].shape)[::-1]  # invert zyx to xyz
            tomo_px_size = img.attrs["EMAN.apix_x"].item()

        # shift to center
        coords = ((shape * tomo_px_size / 2) + (coords * px_size)) / px_size

    poseset = PoseSet(
        position=coords,
        experiment_id=name,
        pixel_spacing=px_size,
        source=json_path,
        features=features,
    )
    return validate_poseset(poseset, coerce=True)
