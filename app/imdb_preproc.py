import pandas as pd


def imdb_set_datatypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preproc: change data types

    param: df: imdb dataset as a pd dataframe
    returns: df: processed dataframe
    """
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df["budget"] = pd.to_numeric(df["budget"], errors="coerce")

    return df


imdb_preproc_list = [
    imdb_set_datatypes,
]
