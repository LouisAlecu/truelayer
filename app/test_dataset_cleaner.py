import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
import numpy as np
from dataset_cleaner import DatasetCleaner


class TestDatasetCleanerNoMissingValues1(unittest.TestCase):
    def setUp(self) -> None:
        self._data = {
            "rnd_col_1": ["2016-12-06T00:26:47+0000", "2016-12-27T05:11:42+0000"],
            "rnd_col_2": ["2017-01-01T03:44:45+0000", "2017-01-28T19:26:56+0000"],
        }
        input_df = pd.DataFrame(self._data)
        self._dataset_cleaner = DatasetCleaner(input_df)

    def test_check_missing_values_1(self) -> None:
        """
        Test if DatasetCleaner.check_missing_values for the case: no missing values
        """
        expected_data = {
            **self._data,
            "no_missing_rnd_col_1": [True, True],
        }
        expected_df = pd.DataFrame(expected_data)
        self._dataset_cleaner.check_missing_values(columns=["rnd_col_1"])
        assert_frame_equal(self._dataset_cleaner.df, expected_df)

    def test_get_cleaned_dataframe_1(self) -> None:
        """
        Test if DatasetCleaner.get_cleaned_dataframe for the case: no missing values
        """
        expected_data = self._data
        expected_df = pd.DataFrame(expected_data)
        self._dataset_cleaner.check_missing_values(columns=["rnd_col_1"])
        cleaned_df = self._dataset_cleaner.get_cleaned_dataframe()
        assert_frame_equal(cleaned_df, expected_df)


class TestDatasetCleanerNoMissingValues2(unittest.TestCase):
    """
    Input data has no missing data, but multiple columns as input
    """

    def setUp(self) -> None:
        self._data = {
            "rnd_col_1": ["2016-12-06T00:26:47+0000", "2016-12-27T05:11:42+0000"],
            "rnd_col_2": ["2017-01-01T03:44:45+0000", "2017-01-28T19:26:56+0000"],
            "rnd_col_3": ["class1", "class2"],
        }
        input_df = pd.DataFrame(self._data)
        self._dataset_cleaner = DatasetCleaner(input_df)

    def test_check_missing_values_1(self) -> None:
        """
        Test if DatasetCleaner.check_missing_values for the case: no missing values, but multiple columns as input
        """
        expected_data = {
            **self._data,
            "no_missing_rnd_col_1": [True, True],
            "no_missing_rnd_col_2": [True, True],
            "no_missing_rnd_col_3": [True, True],
        }
        expected_df = pd.DataFrame(expected_data)
        self._dataset_cleaner.check_missing_values(
            columns=["rnd_col_1", "rnd_col_2", "rnd_col_3"]
        )
        assert_frame_equal(self._dataset_cleaner.df, expected_df)

    def test_get_cleaned_dataframe_1(self) -> None:
        """
        Test if DatasetCleaner.get_cleaned_dataframe for the case: no missing values, but multiple columns as input
        """
        expected_data = self._data
        expected_df = pd.DataFrame(expected_data)
        self._dataset_cleaner.check_missing_values(
            columns=["rnd_col_1", "rnd_col_2", "rnd_col_3"]
        )
        cleaned_df = self._dataset_cleaner.get_cleaned_dataframe()
        assert_frame_equal(cleaned_df, expected_df)


class TestDatasetCleanerContainsMissingValues1(unittest.TestCase):
    """
    Input data contains missing data in 1 column in 1 row
    """

    def setUp(self) -> None:
        self._data = {
            "rnd_col_1": ["2016-12-06T00:26:47+0000", "2016-12-27T05:11:42+0000"],
            "rnd_col_2": ["2017-01-01T03:44:45+0000", "2017-01-28T19:26:56+0000"],
            "rnd_col_3": ["class1", np.nan],
        }
        input_df = pd.DataFrame(self._data)
        self._dataset_cleaner = DatasetCleaner(input_df)

    def test_check_missing_values_1(self) -> None:
        """
        Test if DatasetCleaner.check_missing_values for the case: missing data in 1 column in 1 row
        """
        expected_data = {
            **self._data,
            "no_missing_rnd_col_1": [True, True],
            "no_missing_rnd_col_2": [True, True],
            "no_missing_rnd_col_3": [True, False],
        }
        expected_df = pd.DataFrame(expected_data)
        self._dataset_cleaner.check_missing_values(
            columns=["rnd_col_1", "rnd_col_2", "rnd_col_3"]
        )
        assert_frame_equal(self._dataset_cleaner.df, expected_df)

    def test_get_cleaned_dataframe_1(self) -> None:
        """
        Test if DatasetCleaner.get_cleaned_dataframe for the case: missing data in 1 column in 1 row
        """
        expected_data = {
            "rnd_col_1": ["2016-12-06T00:26:47+0000"],
            "rnd_col_2": ["2017-01-01T03:44:45+0000"],
            "rnd_col_3": ["class1"],
        }
        expected_df = pd.DataFrame(expected_data)
        self._dataset_cleaner.check_missing_values(
            columns=["rnd_col_1", "rnd_col_2", "rnd_col_3"]
        )
        cleaned_df = self._dataset_cleaner.get_cleaned_dataframe()
        assert_frame_equal(cleaned_df, expected_df)


class TestDatasetCleanerContainsMissingValues2(unittest.TestCase):
    """
    Input data contains missing data in multiple columns and multiple rows
    """

    def setUp(self) -> None:
        self._data = {
            "rnd_col_1": [
                "2016-12-06T00:26:47+0000",
                np.nan,
                "2016-12-09T05:05:42+0000",
            ],
            "rnd_col_2": [
                "2017-01-01T03:44:45+0000",
                "2017-01-28T19:26:56+0000",
                np.nan,
            ],
            "rnd_col_3": ["class1", np.nan, np.nan],
        }
        input_df = pd.DataFrame(self._data)
        self._dataset_cleaner = DatasetCleaner(input_df)

    def test_check_missing_values_1(self) -> None:
        """
        Test if DatasetCleaner.check_missing_values for the case: missing values in multiple columns and multiple rows
        """
        expected_data = {
            **self._data,
            "no_missing_rnd_col_1": [True, False, True],
            "no_missing_rnd_col_2": [True, True, False],
            "no_missing_rnd_col_3": [True, False, False],
        }
        expected_df = pd.DataFrame(expected_data)
        self._dataset_cleaner.check_missing_values(
            columns=["rnd_col_1", "rnd_col_2", "rnd_col_3"]
        )
        assert_frame_equal(self._dataset_cleaner.df, expected_df)

    def test_get_cleaned_dataframe_1(self) -> None:
        """
        Test if DatasetCleaner.get_cleaned_dataframe for the case: missing values in multiple columns and multiple rows
        """
        expected_data = {
            "rnd_col_1": ["2016-12-06T00:26:47+0000"],
            "rnd_col_2": ["2017-01-01T03:44:45+0000"],
            "rnd_col_3": ["class1"],
        }
        expected_df = pd.DataFrame(expected_data)
        self._dataset_cleaner.check_missing_values(
            columns=["rnd_col_1", "rnd_col_2", "rnd_col_3"]
        )
        cleaned_df = self._dataset_cleaner.get_cleaned_dataframe()
        assert_frame_equal(cleaned_df, expected_df)


def suite() -> None:
    """
    Creates the test suites to be ran.
    """
    suite = unittest.TestSuite()
    suite.addTest(TestDatasetCleanerNoMissingValues1("test_check_missing_values_1"))
    suite.addTest(TestDatasetCleanerNoMissingValues1("test_get_cleaned_dataframe_1"))
    suite.addTest(TestDatasetCleanerNoMissingValues2("test_check_missing_values_1"))
    suite.addTest(TestDatasetCleanerNoMissingValues2("test_get_cleaned_dataframe_1"))

    suite.addTest(
        TestDatasetCleanerContainsMissingValues1("test_check_missing_values_1")
    )
    suite.addTest(
        TestDatasetCleanerContainsMissingValues1("test_get_cleaned_dataframe_1")
    )
    suite.addTest(
        TestDatasetCleanerContainsMissingValues2("test_check_missing_values_1")
    )
    suite.addTest(
        TestDatasetCleanerContainsMissingValues2("test_get_cleaned_dataframe_1")
    )
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
