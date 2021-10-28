import pandas as pd
from dataset_cleaner import DatasetCleaner
from files_handler import write_wiki_to_csv, read_wiki, read_imdb_movies_metadata
from imdb_preproc import imdb_preproc_list
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres@truelayer_db:5432/truelayer")


def merge_imdb_and_wiki(df_imdb: pd.DataFrame, df_wiki: pd.DataFrame) -> pd.DataFrame:
    """
    Merges the imdb and wiki dataframes based on original title and title from imdb dataset to title in wiki dataset.

    param: df_imdb: pandas DF for the imdb dataset
    param: df_wiki: pandas DF for the wiki dataset
    returns: df_joined: pandas DF with the datasets merged
    """
    # Because this function is very specific to merging these 2 datasets we expect some specific columns
    # to be present in the 2 dataframes
    msg = "Column {} not in the {}, dataframe columns."
    assert "title" in df_imdb, msg.format("title", "imdb")
    assert "original_title" in df_imdb, msg.format("original_title", "imdb")
    assert "title" in df_wiki, msg.format("title", "wiki")
    assert "url" in df_wiki, msg.format("url", "wiki")
    # We merge df_imdb with df_wiki first on (title, title) and then on (original_title, title)
    # Some wikipedia pages could contain the original_title rather than the title
    # Then, we clean the datasets and concatenate them, then drop duplicates

    # This will result in a dataframe that contains all the rows from imdb with a wikipedia url if it exists
    df_joined_on_title = df_imdb.merge(df_wiki, on="title", how="left")
    df_joined_on_original_title = pd.merge(
        df_imdb, df_wiki, how="left", left_on=["original_title"], right_on=["title"]
    )
    df_joined_on_original_title = df_joined_on_original_title.rename(
        columns={"title_x": "title"}
    )
    df_joined_on_original_title = df_joined_on_original_title.drop("title_y", axis=1)
    df_joined = pd.concat(
        [df_joined_on_title, df_joined_on_original_title]
    ).drop_duplicates(["title", "original_title", "release_date"], keep="last")

    return df_joined


def calculate_columns_ratio(
    df: pd.DataFrame,
    numerator: str = "budget",
    denominator: str = "revenue",
    resulting_col_name: str = "ratio",
) -> pd.DataFrame:
    """
    Calculate num/denom and stores it into a column called ratio.

    returns: df with added column called ratio
    """
    msg = "Column {} not in the dataframe columns."
    assert numerator in df.columns, msg.format(numerator)
    assert denominator in df.columns, msg.format(denominator)
    assert (
        resulting_col_name not in df.columns
    ), f"Your resulting column name {resulting_col_name} is already present in the dataframe columns. You will override existing data. Do this outside this function if it is expected behaviour."

    df[resulting_col_name] = round(df[numerator] / df[denominator], 3)

    return df


def imdb_run_preproc_and_cleaner(df_imdb: pd.DataFrame) -> pd.DataFrame:
    """
    Running the preprocessing and cleaner for the imdb dataset

    returns: cleaned df_imdb
    """
    # Get the imdb dataset
    # Clean the imdb dataset
    for preproc in imdb_preproc_list:
        df_imdb = preproc(df_imdb)

    dataset_cleaner_imdb = DatasetCleaner(df_imdb)

    # We make an assumption that missing values for the 4 columns means we have no data for them, so we remove the rows
    # We make the assumption that 0 budget actually means we don't know the budget, as we can't have 0 budget when creating a movie
    # We also remove the rows where revenue equals to 0 because we can't do a budget to revenue ratio with a revenue 0 because of division by zero.
    dataset_cleaner_imdb.check_missing_values(
        ["revenue", "budget", "title", "original_title"]
    )
    dataset_cleaner_imdb.check_zero_values(["revenue", "budget"])
    dataset_cleaner_imdb.write_to_csv("./logs_dataset_cleaner_result_imdb.csv")

    df_imdb = dataset_cleaner_imdb.get_cleaned_dataframe()

    return df_imdb


def wiki_run_preproc_and_cleaner(df_wiki: pd.DataFrame) -> pd.DataFrame:
    """
    Running the preprocessing and cleaner for the wiki dataset

    returns: cleaned df_wiki
    """
    # Get the wiki dataset
    # Clean the wiki dataset
    df_wiki = read_wiki()
    dataset_cleaner_wiki = DatasetCleaner(df_wiki)
    dataset_cleaner_wiki.check_missing_values(["title", "url"])
    dataset_cleaner_wiki.write_to_csv("./logs_dataset_cleaner_result_wiki.csv")
    df_wiki = dataset_cleaner_wiki.get_cleaned_dataframe()

    return df_wiki


def run_process() -> None:
    """
    Starting point for the pipeline
    """
    print("Starting proccess")
    print("Reading imdb")
    df_imdb = read_imdb_movies_metadata()
    print("Running preproc and dataset cleaner for imdb.")
    df_imdb = imdb_run_preproc_and_cleaner(df_imdb)

    print("Reading wiki")
    df_wiki = read_wiki()
    print("Running preproc and dataset cleaner for wiki")
    df_wiki = wiki_run_preproc_and_cleaner(df_wiki)

    print("Merging datasets")
    df_joined = merge_imdb_and_wiki(df_imdb, df_wiki)
    print("Calculating ratio budget to revenue: budget/revenue")
    df_joined = calculate_columns_ratio(
        df_joined, numerator="budget", denominator="revenue", resulting_col_name="ratio"
    )

    df_joined.sort_values(by=["ratio"], inplace=True, ascending=False)
    df_joined = df_joined.head(1000)
    print("Uploading to db.")
    df_joined.to_sql(
        "truelayer_films_result",
        engine,
        schema="truelayer_schema",
        if_exists="replace",
        index=False,
    )
    print("Finished process")
