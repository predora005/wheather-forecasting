# coding: utf-8

import pandas as pd

##################################################
# 日付・時刻の列を先頭に移動する
##################################################
def move_datetime_column_to_top(df):
    """ 日付・時刻の列を先頭に移動する

    Args:
        df(DataFrame) : 変換対象のDataFrame

    Returns:
        DataFrame : 変換後のDataFrame
    """
    new_columns = ['日付', '時']
    for col in df.columns:
        if (col != '日付') and (col != '時'):
            new_columns.append(col)
    
    new_df = df.loc[:, new_columns]
    
    return new_df

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