import pandas as pd


class DatasetCleaner:
    def __init__(self, df):
        """
        Constructor that receives the dataframe to instantiate the DatasetCleaner class
        """
        self._df = df
        self._initial_columns = df.columns
        self._tracked_columns = []

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, df):
        self._df = df

    def check_missing_values(self, columns: list) -> None:
        """
        Creates a new column for each of the columns in the columns parameter.
        Each of the new columns state whether there are no missing values in the column they track.
        The new columns' names are computed as "no_missing_{check_col}".

        At the end of the cleaner we write the dataframe to a csv.
        Hence we can see the reason we removed each row based on these new columns.
        We can always go back to see which rows have been removed from the initial dataset.

        To get a full dataframe with the cleaned rows see method get_cleaned_dataframe.

        Input:
        Param:
        Returns:
        """
        for check_col in columns:
            tracking_col_name = f"no_missing_{check_col}"
            # We need the following code line for the method get_cleaned_dataframe such that we can check
            # if all the tracked column have missing values from the required columns or not. If they do
            # then we remove them. If not, we retain them and return in a clean dataframe.
            self._tracked_columns.append(tracking_col_name)
            self._df[tracking_col_name] = True
            self._df.loc[self._df[check_col].isna(), tracking_col_name] = False

    def check_zero_values(self, columns: list) -> None:
        """
        Creates a new column for each of the columns in the columns parameter.
        Each of the new columns state whether there are zero values in the column they track.
        The new columns' names are computed as "no_zero_values_{check_col}".

        At the end of the cleaner we write the dataframe to a csv.
        Hence we can see the reason we removed each row based on these new columns.
        We can always go back to see which rows have been removed from the initial dataset.

        To get a full dataframe with the cleaned rows see method get_cleaned_dataframe.

        Input:
        Param:
        Returns:
        """
        for check_col in columns:
            tracking_col_name = f"no_zero_values_{check_col}"
            # We need the following code line for the method get_cleaned_dataframe such that we can check
            # if all the tracked column have missing values from the required columns or not. If they do
            # then we remove them. If not, we retain them and return in a clean dataframe.
            self._tracked_columns.append(tracking_col_name)
            self._df[tracking_col_name] = True
            self._df.loc[self._df[check_col] == 0, tracking_col_name] = False

    def write_to_csv(
        self, file_path: str = f"./logs_dataset_cleaner_result.csv"
    ) -> None:
        self._df.to_csv(file_path)

    def get_cleaned_dataframe(self) -> pd.DataFrame:
        """
        Returns the dataframe rows where all the tracked columns contain True values.
        The columns returned will be stored in the self._initial_columns attribute, so we can always remove
        the extra columns added by the dataset cleaner

        Returns: result_df: cleaned pandas Dataframe
        """
        result_df = self._df[self._df[self._tracked_columns].all(axis="columns")][
            self._initial_columns
        ]
        return result_df
