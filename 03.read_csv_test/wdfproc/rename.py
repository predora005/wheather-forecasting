# coding: utf-8

import pandas as pd

__COLUMN_MAP = { 
    ('気圧(hPa)', '現地'): '現地気圧(hPa)',
    ('気圧(hPa)', '海面'): '海面気圧(hPa)',
    ('風向・風速(m/s)', '風速'): '風速(m/s)',
    ('風向・風速(m/s)', '風向'): '風向',
    ('雪(cm)', '降雪'): '降雪(cm)',
    ('雪(cm)', '積雪'): '積雪(cm)',
}

##################################################
# DataFrameの列名を変更する(地上気象データ用)
##################################################
def rename_column_ground(df, place_name):
    """ DataFrameの列名を変更する(地上気象データ用)

    Args:
        df          (DataFrame) : 変更対象のデータ
        place_name  (string)    : 地点名

    Returns:
        DataFrame : 列名変更後のデータ
    """
    
    new_columns = []
    for column in df.columns:
        
        # 列名をtupleからstringに変換する
        if column[0] == column[1]:
            # ex) column=('時','時')
            new_name = column[0]
        else:
            # ex) column=('気圧(hPa)','現地')
            new_name = __COLUMN_MAP[column]
            
        # '日付','時'以外は先頭に地点名を付ける
        if new_name in ('日付', '時'):
            new_column = new_name
        else:
            col_str = [place_name, '_', new_name]
            new_column = ''.join(col_str)
        
        new_columns.append(new_column)
    
    df.columns = new_columns
    return df
    

##################################################
# DataFrameの列名を変更する(高層気象データ用)
##################################################
def rename_column_highrise(df, place_name):
    """ DataFrameの列名を変更する(高層気象データ用)

    Args:
        df          (DataFrame) : 変更対象のデータ
        place_name  (string)    : 地点名

    Returns:
        DataFrame : 列名変更後のデータ
    """
    
    new_columns = []
    for column in df.columns:
        
        # '日付','時'以外は先頭に地点名を付ける
        if column in ('日付', '時'):
            new_column = column
        else:
            col_str = [place_name, '_', column]
            new_column = ''.join(col_str)
        
        new_columns.append(new_column)
    
    df.columns = new_columns
    return df
    
