# coding: utf-8

import pandas as pd
    
##################################################
# DataFrameから指定した列のデータを抽出する
##################################################
def extract_from_columns(df, columns):
    """ DataFrameから指定した列のデータを抽出する

    Args:
        df      (DataFrame)                     : 抽出する対象のデータ
        columns (list[tuple(string,string)])    : 列のリスト

    Returns:
        DataFrame : 指定した列を抽出したデータ
    """
    
    extracted_df = df[columns]
    return extracted_df.copy()
    