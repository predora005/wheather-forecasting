# coding: utf-8

import numpy as np
import pandas as pd
import re

##################################################
# 地上気象データから不要データを除去する
##################################################
def drop_unneeded_ground(df):
    """ 地上気象データから不要データを除去する

    Args:
        df(DataFrame) : 対象のDataFrame

    Returns:
        DataFrame : 不要データ除去後のDataFrame
    """
    new_df = df.replace(['--', '×'], np.nan)
    new_df = new_df.dropna(how='all', axis=1)

    return new_df

##################################################
# 高層気象データから不要データを除去する
##################################################
def drop_unneeded_higirise(df):
    """ 高層気象データから不要データを除去する

    Args:
        df(DataFrame) : 対象のDataFrame

    Returns:
        DataFrame : 不要データ除去後のDataFrame
    """
    #new_df = df.dropna(how='any', axis=1)
    
    # 各列がnullの有無を取得する(1行でもnullが含まれていれば有り)
    column_with_null = df.isnull().any()
    
    # 相対湿度がnullの指定気圧面を記憶する
    drop_column_dict = {}
    for column in df.columns:
        result = re.search(r"\D+_(\d+hPa)_相対湿度", column)
        if result:
            pressure = result.group(1)
            drop_column_dict[pressure] = column_with_null[column]
    
    print(drop_column_dict)
    
    # 相対湿度がnullの指定気圧面の列は削除する
    for pressure in drop_column_dict.keys():
        if drop_column_dict[pressure]:
            
            # 削除対象の列をリストに記憶する
            drop_column_list = []
            for column in df.columns:
                if pressure in column:
                    drop_column_list.append(column)
                    
            # 列を削除する
            df = df.drop(columns=drop_column_list)

    return df

##################################################
# 指定したリストの列を除去する
##################################################
def drop_columns(df, columns):
    """ 指定した名称の列を除去する

    Args:
        df(DataFrame) : 対象のDataFrame
        columns(List) : 除去する列の名称リスト

    Returns:
        DataFrame : 除去する列の名称リスト
    """
    
    for drop_col in columns:
        drop_cols = [col for col in df.columns if(drop_col in col)]
        df = df.drop(columns=drop_cols)
    
    return df
    