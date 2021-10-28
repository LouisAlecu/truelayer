import unittest
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal
from app import calculate_columns_ratio, merge_imdb_and_wiki


class TestCalculateColumnsRatio1(unittest.TestCase):
    """
    Test for simple correct input to check the functionality.
    """

    def setUp(self) -> None:
        self._data = {
            "budget": [100, 1000],
            "revenue": [10, 100],
        }
        self._df = pd.DataFrame(self._data)

    def test_calculate_columns_ratio_1(self) -> None:
        expected_df = pd.DataFrame({**self._data, "ratio": [10.0, 10.0]})

        result_df = calculate_columns_ratio(self._df)
        assert_frame_equal(expected_df, result_df)


class TestCalculateColumnsRatio2(unittest.TestCase):
    """
    Test for nans
    """

    def setUp(self) -> None:
        self._data = {
            "budget": [0, 1000],
            "revenue": [0, 100],
        }
        self._df = pd.DataFrame(self._data)

    def test_calculate_columns_ratio_1(self) -> None:
        expected_df = pd.DataFrame({**self._data, "ratio": [np.nan, 10.0]})

        result_df = calculate_columns_ratio(self._df)
        assert_frame_equal(expected_df, result_df)


class TestCalculateColumnsRatio3(unittest.TestCase):
    """
    Test for infinity
    """

    def setUp(self) -> None:
        self._data = {
            "budget": [100, 100],
            "revenue": [0, 0],
        }
        self._df = pd.DataFrame(self._data)

    def test_calculate_columns_ratio_1(self) -> None:
        expected_df = pd.DataFrame({**self._data, "ratio": [np.inf, np.inf]})

        result_df = calculate_columns_ratio(self._df)
        assert_frame_equal(expected_df, result_df)


class TestMergeImdbAndWiki1(unittest.TestCase):
    """
    Simple test to check functionality with correct input.
    """

    def setUp(self) -> None:
        self._imdb_data = {
            "title": ["title1", "title2"],
            "original_title": ["title1", "title2"],
            "release_date": ["date1", "date2"],
        }
        self._wiki_data = {
            "url": ["url1", "url2"],
            "title": ["title1", "title2"],
        }
        self._imdb_df = pd.DataFrame(self._imdb_data)
        self._wiki_df = pd.DataFrame(self._wiki_data)

    def test_merge_imdb_and_wiki_1(self) -> None:
        expected_df = pd.DataFrame({**self._imdb_data, "url": self._wiki_data["url"]})
        print(self._wiki_df)
        print(self._imdb_df)
        result_df = merge_imdb_and_wiki(self._imdb_df, self._wiki_df)
        assert_frame_equal(expected_df, result_df)


class TestMergeImdbAndWiki2(unittest.TestCase):
    """
    Test for different string in title field, but same in original_title
    """

    def setUp(self) -> None:
        self._imdb_data = {
            "title": ["titleDifferent", "title2"],
            "original_title": ["title1", "title2"],
            "release_date": ["date1", "date2"],
        }
        self._wiki_data = {
            "url": ["url1", "url2"],
            "title": ["title1", "title2"],
        }
        self._imdb_df = pd.DataFrame(self._imdb_data)
        self._wiki_df = pd.DataFrame(self._wiki_data)

    def test_merge_imdb_and_wiki_1(self) -> None:
        expected_df = pd.DataFrame({**self._imdb_data, "url": self._wiki_data["url"]})
        print(self._wiki_df)
        print(self._imdb_df)
        result_df = merge_imdb_and_wiki(self._imdb_df, self._wiki_df)
        print(result_df)
        assert_frame_equal(expected_df, result_df)


class TestMergeImdbAndWiki3(unittest.TestCase):
    """
    Test for different string in title field, different in original_title
    """

    def setUp(self) -> None:
        self._imdb_data = {
            "title": ["titleDifferent", "title2"],
            "original_title": ["titleDifferent", "title2"],
            "release_date": ["date1", "date2"],
        }
        self._wiki_data = {
            "url": ["url1", "url2"],
            "title": ["title1", "title2"],
        }
        self._imdb_df = pd.DataFrame(self._imdb_data)
        self._wiki_df = pd.DataFrame(self._wiki_data)

    def test_merge_imdb_and_wiki_1(self) -> None:
        expected_df = pd.DataFrame({**self._imdb_data, "url": [np.nan, "url2"]})
        print(self._wiki_df)
        print(self._imdb_df)
        result_df = merge_imdb_and_wiki(self._imdb_df, self._wiki_df)
        print(result_df)
        assert_frame_equal(expected_df, result_df)


def suite() -> None:
    """
    Creates the test suites to be ran.
    """
    suite = unittest.TestSuite()
    suite.addTest(TestCalculateColumnsRatio1("test_calculate_columns_ratio_1"))
    suite.addTest(TestCalculateColumnsRatio2("test_calculate_columns_ratio_1"))
    suite.addTest(TestCalculateColumnsRatio3("test_calculate_columns_ratio_1"))
    suite.addTest(TestMergeImdbAndWiki1("test_merge_imdb_and_wiki_1"))
    suite.addTest(TestMergeImdbAndWiki2("test_merge_imdb_and_wiki_1"))
    suite.addTest(TestMergeImdbAndWiki3("test_merge_imdb_and_wiki_1"))

    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
