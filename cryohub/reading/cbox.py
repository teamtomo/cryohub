import starfile
from cryotypes.poseset import validate_poseset

from ..utils.generic import guess_name
from ..utils.types import PoseSet


def read_cbox(
    cbox_path,
    name_regex=None,
    **kwargs,
):
    data = starfile.read(cbox_path)["cryolo"]
    coords = data[[f"Coordinate{axis}" for axis in "XYZ"]].to_numpy()
    name = guess_name(cbox_path, name_regex)

    poseset = PoseSet(
        position=coords,
        experiment_id=name,
        source=cbox_path,
    )
    return validate_poseset(poseset, coerce=True)
