import pandas as pd


def write_wiki_to_csv(
    xml_file: str = "/workdir/data_wikipedia/enwiki-latest-abstract.xml",
    csv_file: str = "/workdir/data_wikipedia/wiki_data.csv",
) -> None:
    """
    Reads the xml file and outputs it to csv such that it can be loaded much faster later.
    """
    wiki_df = pd.read_xml(xml_file)
    wiki_df.to_csv(csv_file, index=False)


def read_wiki(csv_file: str = "/workdir/data_wikipedia/wiki_data.csv") -> pd.DataFrame:
    """
    Read the wiki csv file into a dataframe.

    Returns:
            the dataframe with the title adjusted by removing
            part of the string and just a subset of columns required by the exercise
    """
    df = pd.read_csv(csv_file)
    df["title"].replace(
        to_replace="^Wikipedia: (.*)$", value=r"\1", regex=True, inplace=True
    )
    df = df[["title", "url"]]
    return df


def read_imdb_movies_metadata(
    csv_file: str = "/workdir/data_imdb/movies_metadata.csv",
) -> None:
    """
    Read the imdb csv file into a dataframe.

    Returns: the dataframe with only a subset of columns
    """
    df = pd.read_csv(csv_file, quotechar='"')
    df = df[
        [
            "title",
            "original_title",
            "budget",
            "revenue",
            "release_date",
            "vote_average",
            "production_companies",
        ]
    ]
    return df
