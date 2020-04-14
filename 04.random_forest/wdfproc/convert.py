# coding: utf-8

import math
import numpy as np
import pandas as pd
import re

__WIND_DIRECTION_TO_ANGLE_MAP = { 
    '東'    : 0.0,
    '東北東': math.pi * 1 / 8,
    '北東'  : math.pi * 2 / 8,
    '北北東': math.pi * 3 / 8,
    '北'    : math.pi * 4 / 8,
    '北北西': math.pi * 5 / 8,
    '北西'  : math.pi * 6 / 8,
    '西北西': math.pi * 7 / 8,
    '西'    : math.pi,
    '西南西': -math.pi * 7 / 8,
    '南西'  : -math.pi * 6 / 8,
    '南南西': -math.pi * 5 / 8,
    '南'    : -math.pi * 4 / 8,
    '南南東': -math.pi * 3 / 8,
    '南東'  : -math.pi * 2 / 8,
    '東南東': -math.pi * 1 / 8,
    #'×'     : 0.0
}

##################################################
# 風速・風向きを数値に変換する
##################################################
def convert_wind(df):
    """ 風速・風向きを数値に変換する

    Args:
        df(DataFrame) : 変換対象のDataFrame

    Returns:
        DataFrame : 変換後のDataFrame
    """
    
    # 風向きを数値に変換する関数
    def to_angle(wind_direction):
        angle = 0.0
        if wind_direction in __WIND_DIRECTION_TO_ANGLE_MAP:
            angle = __WIND_DIRECTION_TO_ANGLE_MAP[wind_direction]
        else:
            anble = 0.0
        return angle
        
    # 風向きを数値に変換する
    wind_dir_cols = [col for col in df.columns if('風向' in col)]
    for col in wind_dir_cols:
        new_col = col + '(角度)'
        df[new_col] = df[col].map(lambda col : to_angle(col))
    
    # 風速のうち無効なデータを0に補正する
    wind_speed_cols = [col for col in df.columns if('風速' in col)]
    for col in wind_speed_cols:
        if df[col].dtype == object:
            df.replace({col: {'×': 0.0}}, inplace=True)
    
    # 風向き・風速を、X,Y方向の風速に変換する
    wind_angle_cols = [col for col in df.columns if('風向(角度)' in col)]
    for angle_col in wind_angle_cols:
        result = re.search(r"(\D+)_風向\(角度\)", angle_col)
        place_name = result.group(1)
        speed_col = place_name + '_' + '風速(m/s)'
        df = df.astype({speed_col: float})
        #print(speed_col)
        #print(df[speed_col].tolist())
        
        wind_x_col = place_name + '_' + '風速(m/s)_X'
        wind_y_col = place_name + '_' + '風速(m/s)_Y'
        #df[wind_x_col] = df[speed_col].values * df[angle_col].values
        df[wind_x_col] = df[speed_col] * np.cos(df[angle_col])
        df[wind_y_col] = df[speed_col] * np.sin(df[angle_col])
    
        # 新しく追加した列の小数点を丸める
        df = df.round({wind_x_col: 3, wind_y_col: 3})

    # 元の風向き・風速を削除する
    df = df.drop(columns=wind_dir_cols)
    df = df.drop(columns=wind_speed_cols)
    df = df.drop(columns=wind_angle_cols)
    
    return df