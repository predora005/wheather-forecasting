# coding: utf-8

import numpy as np
from sklearn.preprocessing import MinMaxScaler

##################################################
# Max-Minスケール化(0〜1の範囲に収まるように標準化)
##################################################
def max_min_scale(train_data, test_data=None):
    
    scaler = MinMaxScaler()
    train_scaled = scaler.fit_transform(train_data)
    
    if test_data is not None:
        test_scaled  = scaler.transform(test_data)
    else:
        test_scaled = None
    
    return scaler, train_scaled, test_scaled
    
##################################################
# NaNを平均値で置換する
##################################################
def fill_na_avg(df, inplace=True):
    """ NaNを平均値で置換する

    Args:
        df(DataFrame) : 変換対象のDataFrame
        inplace(bool) : 元のDataFrameを変更するか否か

    Returns:
        DataFrame : 変換後のDataFrame
    """
    if inplace:
        new_df = df
    else:
        new_df = df.copy()
    
    # 変換する列と値のディクショナリを作成する
    fillna_dict = {}
    has_nan_columns = new_df.isnull().any()
    for col in has_nan_columns.index:
        
        # NaNが含まれる列のみ変換対象とする
        has_nan = has_nan_columns[col]
        if has_nan:
            
            typ = new_df[col].dtype
            if (typ == np.float32) or (typ == np.float64) :
                # データ型がfloatの場合は平均値で変換する
                avg = new_df[col].mean()
                fillna_dict[col] = avg
            elif (typ == np.int32) or (typ ==  np.int64) :
                # データ型がintの場合は平均値に最も近い整数値で変換する
                avg = new_df[col].mean()
                fillna_dict[col] = int(np.around(avg))
            
    # NaNを置換する
    new_df = new_df.fillna(fillna_dict)
    
    return new_df
    
##################################################
# 浮動小数点を32ビットに変更する
##################################################
def type_to_float32(df, inplace=True):
    """ 浮動小数点を32ビットに変更する

    Args:
        df(DataFrame) : 変換対象のDataFrame
        inplace(bool) : 元のDataFrameを変更するか否か

    Returns:
        DataFrame : 変換後のDataFrame
    """
    if inplace:
        new_df = df
    else:
        new_df = df.copy()
    
    # 変換する列と型のディクショナリを作成する
    astype_dict = {}
    for col in new_df.columns:
        typ = new_df[col].dtype
        if typ == object:
            # object -> np.float32
            astype_dict[col] = np.float32
        elif typ == np.float64:
            # np.float64 -> np.float32
            astype_dict[col] = np.float32
    
    # データ型を変換する
    new_df = new_df.astype(astype_dict, copy=False)
    
    return new_df
    