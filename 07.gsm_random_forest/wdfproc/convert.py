# coding: utf-8

import math
from enum import Enum
import numpy as np
import pandas as pd
import re

# 風向きをラジアンに変換するマップ
__WIND_DIRECTION_TO_ANGLE_MAP = {
    '東'    : 0.0,              '東北東': math.pi * 1 / 8,  '北東'  : math.pi * 2 / 8,
    '北北東': math.pi * 3 / 8,  '北'    : math.pi * 4 / 8,  '北北西': math.pi * 5 / 8,
    '北西'  : math.pi * 6 / 8,  '西北西': math.pi * 7 / 8,  '西'    : math.pi,
    '西南西': -math.pi * 7 / 8, '南西'  : -math.pi * 6 / 8, '南南西': -math.pi * 5 / 8,
    '南'    : -math.pi * 4 / 8, '南南東': -math.pi * 3 / 8, '南東'  : -math.pi * 2 / 8,
    '東南東': -math.pi * 1 / 8,
    #'×'     : 0.0
}

# 天気を変換する際のモード
class WeatherConvertMode(Enum):
    Coarse = 1      # 粗い
    Fine = 2        # 細かい
    RainOrNot = 3   # 雨か否かの二者択一

# 天気を整数値に変換するマップ
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

# 天気を変換するマップ(粗め)
__WEATHER_REPLACE_MAP_COARSE = {
    1:  0, 2:  0,           # 快晴, 晴れ    -> 晴れ
    3:  1, 4:  1,           # 薄曇, 曇り    -> くもり
    8:  2, 9:  2, 10: 2,    # 霧, 霧雨, 雨                  -> 雨
    11: 2, 12: 2, 13: 2,    # みぞれ, 雪, あられ            -> 雨
    14: 2, 16: 2, 17: 2,    # ひょう, しゅう雨, 着氷性の雨  -> 雨
    18: 2, 19: 2, 22: 2,    # 着氷性の霧雨, しゅう雪, 霧雪  -> 雨
    23: 2, 24: 2, 28: 2,    # 凍雨, 細氷, もや              -> 雨
    101:2,                  # 降水                          -> 雨
    5:  3, 6:  3, 7:  3,    # 煙霧, 砂じん嵐, 地ふぶき  -> その他
    15: 3, 0:  3            # 雷, 不明                  -> その他
}

# 天気を変換するマップ(細かめ)
__WEATHER_REPLACE_MAP_FINE = {
    1:  0,                  # 快晴  -> 快晴
    2:  1,                  # 晴れ  -> 晴れ
    3:  2,                  # 薄曇  -> 薄曇
    4:  3,                  # 曇り  -> 曇り
    8:  4, 9:  4, 10: 4,    # 霧, 霧雨, 雨                  -> 雨
    11: 4, 12: 4, 13: 4,    # みぞれ, 雪, あられ            -> 雨
    14: 4, 16: 4, 17: 4,    # ひょう, しゅう雨, 着氷性の雨  -> 雨
    18: 4, 19: 4, 22: 4,    # 着氷性の霧雨, しゅう雪, 霧雪  -> 雨
    23: 4, 24: 4, 28: 4,    # 凍雨, 細氷, もや              -> 雨
    101:4,                  # 降水                          -> 雨
    5:  5, 6:  5, 7:  5,    # 煙霧, 砂じん嵐, 地ふぶき  -> その他
    15: 5, 0:  5            # 雷, 不明                  -> その他
}

# 天気を変換するマップ(雨か否かの二者択一)
__WEATHER_REPLACE_MAP_RAIN_OR_NOT= {
    1:  0, 2:  0,           # 快晴, 晴れ    -> 雨以外
    3:  0, 4:  0,           # 薄曇, 曇り    -> 雨以外
    8:  1, 9:  1, 10: 1,    # 霧, 霧雨, 雨                  -> 雨
    11: 1, 12: 1, 13: 1,    # みぞれ, 雪, あられ            -> 雨
    14: 1, 16: 1, 17: 1,    # ひょう, しゅう雨, 着氷性の雨  -> 雨
    18: 1, 19: 1, 22: 1,    # 着氷性の霧雨, しゅう雪, 霧雪  -> 雨
    23: 1, 24: 1, 28: 1,    # 凍雨, 細氷, もや              -> 雨
    101:1,                  # 降水                          -> 雨
    5:  0, 6:  0, 7:  0,    # 煙霧, 砂じん嵐, 地ふぶき  -> 雨以外
    15: 0, 0:  0            # 雷, 不明                  -> 雨以外
}

# 雲量を浮動小数点数に変換するマップ
__CLOUD_VOLUME_TO_FLOAT_MAP = {
    '0+'  : 0.5, 
    '10-' : 9.5,
}

##################################################
# 天気記号を数値に変換する
##################################################
def convert_symbol_to_number(df, inplace=True):
    """ 天気記号を数値に変換する

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

    # 天気記号を数値に変換する
    def to_number(element):
        if type(element) is str:
            if ')' in element:
                value = element.replace(')', '')
            elif ']' in element:
                value = element.replace(']', '')
            else:
                value = element
        else:
            value = element
            
        return value

    # 天気を整数値に変換する
    for col in df.columns:
        new_df[col] = new_df[col].map(lambda element : to_number(element))
    
    return new_df

##################################################
# 風速・風向きをX,Y方向のベクトルに変換する(地上気象データ用)
##################################################
def convert_wind_to_vector_ground(df, inplace=True):
    """ 風速・風向きをX,Y方向のベクトルに変換する
        (地上気象データ用)

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

        wind_x_col = place_name + '_' + '風速(m/s)_X'
        wind_y_col = place_name + '_' + '風速(m/s)_Y'
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
        value = 0
        if name in __WEATHER_TO_INT_MAP:
            value = __WEATHER_TO_INT_MAP[name]
        else:
            value = 0
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
# 天気を指定した境界値で分類する
##################################################
def classify_weather_boundary(df, boudaries=None, colums=None, inplace=True):
    """ 天気を指定した境界値で分類する

    Args:
        df(DataFrame)   : 変換対象のDataFrame
        boudaries(List) : 境界値のリスト
        columns(List)   : 変換対象の列名
        inplace(bool)   : 元のDataFrameを変更するか否か

    Returns:
        DataFrame : 変換後のDataFrame
    """
    
    # 元のDataFrameを上書きするか否か
    if inplace:
        new_df = df
    else:
        new_df = df.copy()
    
    # 境界値が未設定の場合はデフォルト値を使用する
    if boudaries is None:
        boudaries = [3, 10]
    
    # 天気を境界値で分類する関数
    def classify(weather):
        class_value = -1
        for i, boundary in enumerate(boudaries):
            # 境界値未満だったらループ離脱
            if boundary > weather:
                class_value = i
                break
            
        # 全ての境界値以上の場合
        if class_value < 0:
            class_value = len(boudaries)
        
        return class_value
    
    # 列名が未設定の場合は、名称に天気を含む列を抽出する
    if colums is None:
        weather_cols = [col for col in new_df.columns if('天気' in col)]
    else:
        weather_cols = colums
    
    # 天気を指定した境界値で分類する
    for col in weather_cols:
        new_df[col] = new_df[col].map(lambda col : classify(col))
    
    return new_df

##################################################
# 天気を指定したマップで置換する
##################################################
def replace_weather(df, rmap=None, columns=None, mode=WeatherConvertMode.Coarse, inplace=True):
    """ 天気を指定したマップで置換する

    Args:
        df(DataFrame)   : 変換対象のDataFrame
        rmap(Dict)      : 変換用のマップ
        columns(List)   : 変換対象の列名
        inplace(bool)   : 元のDataFrameを変更するか否か

    Returns:
        DataFrame : 変換後のDataFrame
    """
    
    # 元のDataFrameを上書きするか否か
    if inplace:
        new_df = df
    else:
        new_df = df.copy()
    
    # 境界値が未設定の場合はデフォルト値を使用する
    if rmap is None:
        if mode == WeatherConvertMode.Fine:
            rmap = __WEATHER_REPLACE_MAP_FINE
        elif mode == WeatherConvertMode.RainOrNot:
            rmap = __WEATHER_REPLACE_MAP_RAIN_OR_NOT
        else:
            rmap = __WEATHER_REPLACE_MAP_COARSE
    
    # 列名が未設定の場合は、名称に天気を含む列を抽出する
    if columns is None:
        weather_cols = [col for col in new_df.columns if('天気' in col)]
    else:
        weather_cols = columns
    
    # 天気を指定したマップで置換する
    for col in weather_cols:
        new_df = new_df.replace({col: rmap})

    return new_df

##################################################
# 風速・風向きをX,Y方向のベクトルに変換する(高層気象データ用)
##################################################
def convert_wind_to_vector_highrise(df, inplace=True):
    """ 風速・風向きをX,Y方向のベクトルに変換する
        (高層気象データ用)

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
    
    # 風向きを度数(°)からラジアンに変換する関数
    def to_radian(wind_deg):
        radian = (-wind_deg + 90)/180 * math.pi
        return radian
    
    wind_radian_cols = []
    
    # 風向きを度数(°)からラジアンに変換する
    wind_dir_cols = [col for col in new_df.columns if('風向' in col)]
    for col in wind_dir_cols:
        new_col = col + '(rad)'
        new_df[new_col] = new_df[col].map(lambda col : to_radian(col))
        wind_radian_cols.append(new_col)

    # 風速のうち無効なデータを0に補正する
    wind_speed_cols = [col for col in new_df.columns if('風速' in col)]
    for col in wind_speed_cols:
        if df[col].dtype == object:
            new_df.replace({col: ['−', '静穏']}, 0.0, inplace=True)

    # 風向き・風速を、X,Y方向の風速に変換する
    for radian_col in wind_radian_cols:
        result = re.search(r"(.+)_風向.*\(rad\)", radian_col)
        prifix = result.group(1)
        speed_col = prifix + '_' + '風速(m/s)'
        new_df = new_df.astype({speed_col: float})
        
        wind_x_col = prifix + '_' + '風速(m/s)_X'
        wind_y_col = prifix + '_' + '風速(m/s)_Y'
        new_df[wind_x_col] = new_df[speed_col] * np.cos(df[radian_col])
        new_df[wind_y_col] = new_df[speed_col] * np.sin(df[radian_col])

        # 新しく追加した列の小数点を丸める
        new_df = new_df.round({wind_x_col: 3, wind_y_col: 3})

    # 元の風向き・風速を削除する
    new_df = new_df.drop(columns=wind_dir_cols)
    new_df = new_df.drop(columns=wind_speed_cols)
    new_df = new_df.drop(columns=wind_radian_cols)

    return new_df
    