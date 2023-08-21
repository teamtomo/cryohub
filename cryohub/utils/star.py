import pandas as pd

from .constants import Relion


def extract_optics(df):
    optics_headers = [
        h for h in Relion.POSSIBLE_OPTICS_GROUP_HEADERS if h in df.columns
    ]
    if Relion.OPTICS_GROUP_HEADER in df.columns:
        optic_groups = (
            df.get([Relion.OPTICS_GROUP_HEADER] + optics_headers)
            .drop_duplicates()
            .reset_index(drop=True)
        )
    else:
        if optics_headers:
            df[Relion.OPTICS_GROUP_HEADER] = df.groupby(optics_headers).ngroup()
            optic_groups = (
                df.get([Relion.OPTICS_GROUP_HEADER, *optics_headers])
                .drop_duplicates()
                .reset_index(drop=True)
            )
        else:
            # needed because grouby needs at least a column
            optic_groups = pd.DataFrame({Relion.OPTICS_GROUP_HEADER: [0]})
            df[Relion.OPTICS_GROUP_HEADER] = 0

    df = df.drop(columns=optics_headers, errors="ignore")
    data = {"optics": optic_groups, "particles": df}
    return data


def merge_optics(data_dict):
    return data_dict["particles"].merge(
        data_dict["optics"], on=Relion.OPTICS_GROUP_HEADER
    )
