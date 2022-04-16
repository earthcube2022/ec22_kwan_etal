import re
import pandas as pd


def remove_bracket_text(df):
    """remove trailing text inside brackets."""
    df.replace(r" *\[.*\] *$", "", regex=True, inplace=True)
    return df


def remove_whitespace(df):
    """remove leading and trailing spaces from dataframe rows"""
    for col in df.columns:
        # only process string columns
        if df[col].dtype == "object":
            if len(df[df[col].isna()]) > 0:
                df[col].fillna("", inplace=True)
            try:
                df[col] = df[col].map(str.strip)
            except TypeError:
                print('Must call fillna("") before using whitespace_remover.')


def print_df(df, num_rows=5):
    print(df.shape)
    return df.head(num_rows)


def normalize_columns(df, columns_mapping):
    """Replace variations of column name with a standard column name"""
    temp = {}
    for col in df.columns:
        if col in columns_mapping:
            value = columns_mapping[col]
            if value and value == value:
                temp[col] = value

    if len(temp) > 0:
        df.rename(columns=temp, inplace=True)
