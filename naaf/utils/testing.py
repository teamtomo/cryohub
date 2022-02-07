import numpy as np
import pandas as pd
import dask.array as da
from scipy.spatial.transform import Rotation


def assert_data_equal(data1, data2):
    d1 = data1.dict()
    d2 = data2.dict()
    assert d1.keys() == d2.keys(), 'models do not have the same set of fields'
    for field in d1.keys():
        if isinstance(d1[field], (np.ndarray, da.Array)):
            try:
                if not np.allclose(d1[field], d2[field]):
                    raise AssertionError(f'numeric array fields "{field}" are not within error')
            except TypeError:
                if not np.all(d1[field] == d2[field]):
                    raise AssertionError(f'array fields "{field}" are not equal')
        elif isinstance(d1[field], pd.DataFrame):
            assert set(d1[field].columns) == set(d2[field].columns), f'dataframe fields "{field}" have different columns'
            for col in d1[field]:
                if isinstance(d1[field][col][0], Rotation):
                    s_rot = Rotation.concatenate(d1[field][col])
                    o_rot = Rotation.concatenate(d2[field][col])
                    # invert and multiply should give zero
                    back_forth = (s_rot * o_rot.inv()).reduce().as_rotvec()
                    if not np.allclose(back_forth, 0):
                        raise AssertionError(f'Rotation columns "{col}" of field "{field}" are not equivalent')
                else:
                    try:
                        if not np.allclose(d1[field][col], d2[field][col]):
                            raise AssertionError(f'numeric array columns "{col}" of field "{field}" are not within error')
                    except TypeError:
                        if not np.all(d1[field][col] == d2[field][col]):
                            raise AssertionError(f'array columns "{col}" of field "{field}" are not equal')
        else:
            if not d1[field] == d2[field]:
                return False
    return True
