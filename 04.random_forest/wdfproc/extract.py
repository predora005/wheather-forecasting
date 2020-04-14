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
    
##################################################
# DataFrameから指定した要素を含む行を抽出する
##################################################
def extract_row_isin(df, column, values):
    """ DataFrameから指定した要素を含む行を抽出する

    Args:
        df      (DataFrame)     : 抽出する対象のデータ
        column  (string)        : 列の名称
        values  (list[object])  : 指定した要素

    Returns:
        DataFrame : 指定した要素を含む行
    """
    
    extracted_df  = df[df[column].isin(values)]
    return extracted_df.copy()