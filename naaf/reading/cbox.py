from scipy.spatial.transform import Rotation
import starfile

from ..utils.generic import guess_name
from ..utils.constants import Relion


def read_cbox(
    cbox_path,
    name_regex=None,
    **kwargs,
):
    data = starfile.read(cbox_path)['cryolo']
    coords = data[[f'Coordinate{axis}' for axis in 'XYZ']].to_numpy()
    rot = Rotation.identity(len(coords)).as_euler(Relion.EULER)
    name = guess_name(cbox_path, name_regex)
    return coords, rot, {'name': name}
