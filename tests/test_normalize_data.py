import pandas as pd
from pandas._testing import assert_frame_equal
import pytest
import numpy as np

from scripts.normalize_data import (
    remove_bracket_text,
    remove_whitespace,
    normalize_columns
)

class TestRemoveBracketText:
    def test_removes_text_within_brackets_at_end_of_cell(self):
        df = pd.DataFrame(['aa [A]', 'bb [BB]', 'cc [C] ', 'dd  [dd]  '])
        expected = pd.DataFrame(['aa', 'bb', 'cc', 'dd'])

        remove_bracket_text(df)

        assert_frame_equal(df, expected)

    def test_does_not_remove_text_within_brackets_at_start_of_cell(self):
        df = pd.DataFrame(['[A] aa', '[BB] bb', '[C] cc ', '  [dd]  dd '])
        expected = df.copy()

        remove_bracket_text(df)

        assert_frame_equal(df, expected)

    def test_does_not_remove_text_within_brackets_in_middle_of_cell(self):
        df = pd.DataFrame(['aa [A] aa', 'bb [BB] bb', ' cc [C] cc ', ' dd  [dd]  dd '])
        expected = df.copy()

        remove_bracket_text(df)

        assert_frame_equal(df, expected)

    def test_removes_letters_numbers_punctuation_within_brackets(self):
        df = pd.DataFrame(['aa [A A]', 'bb [BB 123]', 'cc [123-456.] '])
        expected = pd.DataFrame(['aa', 'bb', 'cc'])

        remove_bracket_text(df)

        assert_frame_equal(df, expected)


class TestRemoveWhitespaceFromDataframe:
    def test_remove_leading_and_trailing_spaces_from_dataframe(self):
        data = {
            'A': ['A', 'B ', '  C', 'D  ', '  Ed  ', ' 1 '],
            'B': ['Aa', 'Bb ', '  Cc', 'Dd  ', '  Ed Ed  ', ' 11 '],
        }
        df = pd.DataFrame(data)
        data2 = {
            'A': ['A', 'B', 'C', 'D', 'Ed', '1'],
            'B': ['Aa', 'Bb', 'Cc', 'Dd', 'Ed Ed', '11'],
        }
        expected = pd.DataFrame(data2)

        remove_whitespace(df)

        assert_frame_equal(df, expected)

    def test_ignores_numeric_columns(self):
        data = {
            'A': ['A', 'B  ', '  C'],
            'B': [1, 2, 3],
            'C': [1.1, 2.2, 3.3],
        }
        df = pd.DataFrame(data)
        data2 = {
            'A': ['A', 'B', 'C'],
            'B': [1, 2, 3],
            'C': [1.1, 2.2, 3.3],
        }
        expected = pd.DataFrame(data2)

        remove_whitespace(df)

        assert_frame_equal(df, expected)

    def test_handles_empty_strings(self):
        data = {'A': ['A', 'B  ', '  C', ' ']}
        df = pd.DataFrame(data)
        data2 = {'A': ['A', 'B', 'C', '']}
        expected = pd.DataFrame(data2)

        remove_whitespace(df)

        assert_frame_equal(df, expected)

    def test_converts_nan_to_empty_strings(self):
        data = {'A': ['A', 'B  ', '  C', np.nan]}
        df = pd.DataFrame(data)
        data2 = {'A': ['A', 'B', 'C', '']}
        expected = pd.DataFrame(data2)

        remove_whitespace(df)

        assert_frame_equal(df, expected)


class TestNormalizeColumns:
    def test_replace_column_name_with_value_from_columns_mapping(self):
        columns_mapping = {"aa": "A"}
        data = {"aa": [1]}
        df = pd.DataFrame(data)
        data = {"A": [1]}
        expected = pd.DataFrame(data)

        normalize_columns(df, columns_mapping)

        assert_frame_equal(df, expected)

    def test_replace_multiple_column_name_with_value_from_columns_mapping(self):
        columns_mapping = {"aa": "A", "b b": "B"}
        data = {"aa": [1], "b b": [2]}
        df = pd.DataFrame(data)
        data = {"A": [1], "B": [2]}
        expected = pd.DataFrame(data)

        normalize_columns(df, columns_mapping)

        assert_frame_equal(df, expected)

    def test_does_not_affect_columns_not_in_columns_mapping(self):
        columns_mapping = {"aa": "A", "b b": "B"}
        data = {"aa": [1], "b b": [2], "cc": [3]}
        df = pd.DataFrame(data)
        data = {"A": [1], "B": [2], "cc": [3]}
        expected = pd.DataFrame(data)

        normalize_columns(df, columns_mapping)

        assert_frame_equal(df, expected)

    def test_does_not_affect_columns_if_columns_mapping_has_no_value(self):
        columns_mapping = {"aa": None, "bb": "", "cc": np.nan}
        data = {"aa": [1], "b b": [2], "cc": [3]}
        df = pd.DataFrame(data)
        expected = pd.DataFrame(data)

        normalize_columns(df, columns_mapping)

        assert_frame_equal(df, expected)
