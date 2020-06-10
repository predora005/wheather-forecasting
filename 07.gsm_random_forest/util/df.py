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
