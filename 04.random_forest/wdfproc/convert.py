# coding: utf-8

import math
import numpy as np
import pandas as pd
import re

__WIND_DIRECTION_TO_ANGLE_MAP = {
    '東'    : 0.0,              '東北東': math.pi * 1 / 8,  '北東'  : math.pi * 2 / 8,
    '北北東': math.pi * 3 / 8,  '北'    : math.pi * 4 / 8,  '北北西': math.pi * 5 / 8,
    '北西'  : math.pi * 6 / 8,  '西北西': math.pi * 7 / 8,  '西'    : math.pi,
    '西南西': -math.pi * 7 / 8, '南西'  : -math.pi * 6 / 8, '南南西': -math.pi * 5 / 8,
    '南'    : -math.pi * 4 / 8, '南南東': -math.pi * 3 / 8, '南東'  : -math.pi * 2 / 8,
    '東南東': -math.pi * 1 / 8,
    #'×'     : 0.0
}

__WEATHER_TO_INT_MAP = {
    '快晴'  : 1, 
    '晴れ'  : 2,
    '薄曇'  : 3,
    '曇'    : 4,
    '煙霧'  : 5, 
    '砂じん嵐'  : 6,
    '地ふぶき'  : 7,
    '霧'        : 8,
    '霧雨'      : 9, 
    '雨'        : 10,
    'みぞれ'    : 11,
    '雪'        : 12,
    'あられ'    : 13, 
    'ひょう'    : 14, 
    '雷'        : 15,
    'しゅう雨または止み間のある雨'  : 16,
    '着氷性の雨'    : 17, 
    '着氷性の霧雨'  : 18,
    'しゅう雪または止み間のある雪'  : 19,
    '霧雪'  : 22,
    '凍雨'  : 23,
    '細氷'  : 24,
    'もや'  : 28,
    '降水またはしゅう雨性の降水'    : 101,
}

__CLOUD_VOLUME_TO_FLOAT_MAP = {
    '0+'  : 0.5, 
    '10-' : 9.5,
}

##################################################
# 風速・風向きをX,Y方向のベクトルに変換する
##################################################
def convert_wind_to_vector(df, inplace=True):
    """ 風速・風向きをX,Y方向のベクトルに変換する

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
    
    # 風向きを数値に変換する関数
    def to_angle(wind_direction):
        angle = 0.0
        if wind_direction in __WIND_DIRECTION_TO_ANGLE_MAP:
            angle = __WIND_DIRECTION_TO_ANGLE_MAP[wind_direction]
        else:
            anble = 0.0
        return angle

    # 風向きを数値に変換する
    wind_dir_cols = [col for col in new_df.columns if('風向' in col)]
    for col in wind_dir_cols:
        new_col = col + '(角度)'
        new_df[new_col] = new_df[col].map(lambda col : to_angle(col))

    # 風速のうち無効なデータを0に補正する
    wind_speed_cols = [col for col in new_df.columns if('風速' in col)]
    for col in wind_speed_cols:
        if df[col].dtype == object:
            new_df.replace({col: {'×': 0.0}}, inplace=True)

    # 風向き・風速を、X,Y方向の風速に変換する
    wind_angle_cols = [col for col in new_df.columns if('風向(角度)' in col)]
    for angle_col in wind_angle_cols:
        result = re.search(r"(\D+)_風向\(角度\)", angle_col)
        place_name = result.group(1)
        speed_col = place_name + '_' + '風速(m/s)'
        new_df = new_df.astype({speed_col: float})
        #print(speed_col)
        #print(df[speed_col].tolist())

        wind_x_col = place_name + '_' + '風速(m/s)_X'
        wind_y_col = place_name + '_' + '風速(m/s)_Y'
        #df[wind_x_col] = df[speed_col].values * df[angle_col].values
        new_df[wind_x_col] = new_df[speed_col] * np.cos(df[angle_col])
        new_df[wind_y_col] = new_df[speed_col] * np.sin(df[angle_col])

        # 新しく追加した列の小数点を丸める
        new_df = new_df.round({wind_x_col: 3, wind_y_col: 3})

    # 元の風向き・風速を削除する
    new_df = new_df.drop(columns=wind_dir_cols)
    new_df = new_df.drop(columns=wind_speed_cols)
    new_df = new_df.drop(columns=wind_angle_cols)

    return new_df
    
##################################################
# 天気を整数値に変換する
##################################################
def convert_weather_to_interger(df, inplace=True):
    """ 天気を整数値に変換する

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

    # 天気を整数値に変換する関数
    def to_integer(name):
        value = 0.0
        if name in __WEATHER_TO_INT_MAP:
            value = __WEATHER_TO_INT_MAP[name]
        else:
            value = 0.0
        return value

    # 天気を整数値に変換する
    weather_cols = [col for col in new_df.columns if('天気' in col)]
    for col in weather_cols:
        new_df[col] = new_df[col].map(lambda col : to_integer(col))
    
    return new_df

##################################################
# 雲量を浮動小数点数に変換する
##################################################
def convert_cloud_volume_to_float(df, inplace=True):
    """ 雲量を浮動小数点数に変換する

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

    # 雲量を浮動小数点数に変換する
    def to_float(name):
        value = 0.0
        if name in __CLOUD_VOLUME_TO_FLOAT_MAP:
            value = __CLOUD_VOLUME_TO_FLOAT_MAP[name]
        else:
            value = 0.0
        return value

    # 天気を整数値に変換する
    cloud_volume_cols = [col for col in new_df.columns if('雲量' in col)]
    for col in cloud_volume_cols:
        new_df[col] = new_df[col].map(lambda col : to_float(col))
    
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
    
    for col, typ in df.dtypes:
        if typ == object:
            new_df[col] = new_df.astype({col: np.float32})
        elif type == np.float64:
            new_df[col] = new_df.astype({col: np.float32})
        