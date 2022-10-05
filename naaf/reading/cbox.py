import pandas as pd
import starfile
from cryotypes.poseset import PoseSetDataLabels as PSDL
from cryotypes.poseset import validate_poseset_dataframe
from scipy.spatial.transform import Rotation

from ..utils.constants import Relion
from ..utils.generic import guess_name


def read_cbox(
    cbox_path,
    name_regex=None,
    **kwargs,
):
    data = starfile.read(cbox_path)["cryolo"]
    coords = data[[f"Coordinate{axis}" for axis in "XYZ"]].to_numpy()
    rot = Rotation.identity(len(coords)).as_euler(Relion.EULER)
    name = guess_name(cbox_path, name_regex)

    df = pd.DataFrame(
        {
            PSDL.POSITION: coords,
            PSDL.ORIENTATION: rot,
            PSDL.EXPERIMENT_ID: name,
        }
    )
    return validate_poseset_dataframe(df, coerce=True)
