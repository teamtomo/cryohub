import dask.array as da
import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation


def rotations_equal(r1, r2):
    """
    Check if rotations result in the same orientations.

    Quaternions result in the same orientation if they have equal real components,
    and imaginary components with the same absolute value
    """
    q1 = r1.as_quat()
    q2 = r2.as_quat()
    if np.allclose(q1[:, :3], q2[:, :3]) and np.allclose(
        np.abs(q1[:, -1]), np.abs(q2[:, -1])
    ):
        return True
    return False


def assert_dataframe_equal(df1, df2, columns=()):
    df1 = df1[[c for c in df1.columns if c in columns]]
    df2 = df2[[c for c in df2.columns if c in columns]]
    assert set(df1.columns) == set(
        df2.columns
    ), f"dataframes have different columns:\n\t{df1.columns}\n\t{df2.columns}"
    for col in df1:
        if isinstance(df1[col][0], Rotation):
            s_rot = Rotation.concatenate(df1[col])
            o_rot = Rotation.concatenate(df2[col])
            # invert and multiply should give zero in mod pi
            if not rotations_equal(s_rot, o_rot):
                raise AssertionError(f'Rotation columns "{col}" of are not equivalent')
        else:
            try:
                if not np.allclose(df1[col], df2[col]):
                    raise AssertionError(
                        f'numeric array columns "{col}" are not within error tolerance'
                    )
            except TypeError:
                if not np.all(df1[col] == df2[col]):
                    raise AssertionError(f'array columns "{col}" are not equal')


def assert_dataclass_equal(data1, data2, fields=()):
    d1 = {
        field: getattr(data1, field)
        for field in data1.__dataclass_fields__
        if field in fields
    }
    d2 = {
        field: getattr(data2, field)
        for field in data2.__dataclass_fields__
        if field in fields
    }
    assert set(d1.keys()) == set(
        d2.keys()
    ), f"models do not have the same set of fields:\n\t{list(d1)}\n\t{list(d2)}"
    for field in d1:
        if isinstance(d1[field], (np.ndarray, da.Array)):
            try:
                if not np.allclose(d1[field], d2[field]):
                    raise AssertionError(
                        f'numeric array fields "{field}" are not within error'
                    )
            except TypeError:
                if not np.all(d1[field] == d2[field]):
                    raise AssertionError(f'array fields "{field}" are not equal')
        elif isinstance(d1[field], pd.DataFrame):
            assert_dataframe_equal(
                d1[field], d2[field], columns=list(d1[field].columns)
            )
        else:
            if not d1[field] == d2[field]:
                return False
    return True
