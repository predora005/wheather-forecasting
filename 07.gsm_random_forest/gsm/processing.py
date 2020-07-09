# coding: utf-8

import math
from enum import Enum
import numpy as np
import pandas as pd
import re


##################################################
# 天気記号を数値に変換する
##################################################
def thin_out_gsm(df, interval=(2,2), inplace=True):
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
    
    # 列名から緯度,経度を抽出する
    lati_temp = []
    longi_temp = []
    for column in new_df.columns:
        # '[+-]?(?:\d+\.?\d*|\.\d+)'
        # 'Surf_lat38.00_long135.000_海面更正気圧'
        result = re.search(r"Surf_lat(\d+\.\d+)_long(\d+\.\d+)_海面更正気圧", column)
        if result:
            lati = result.group(1)
            longi = result.group(2)

            # 緯度を追加
            if lati not in lati_temp:
                lati_temp.append(lati)
            
            # 経度を追加
            if longi not in longi_temp:
                longi_temp.append(longi)

    # 緯度を間引く
    latitudes = []
    for i in range(0, len(lati_temp), interval[0]):
        latitudes.append(lati_temp[i])
        
    # 経度を間引く
    longitudes = []
    for i in range(0, len(longi_temp), interval[1]):
        longitudes.append(longi_temp[i])
    
    # 指定した緯度,経度を含む列を抽出する
    new_columns = ['日付', '時']
    for column in new_df.columns:
        
        # 列名から緯度,経度を抽出する
        result = re.search(r"(.*)_lat(\d+\.\d+)_long(\d+\.\d+)_(.*)", column)
        if result:
            lati = result.group(2)
            longi = result.group(3)
            
            if (lati in latitudes) and (longi in longitudes):
                new_columns.append(column)
        
    # 指定した列のみのDataFrameを作成する
    new_df = new_df[new_columns]
    
    return new_df

##################################################
# 天気記号を数値に変換する
##################################################
def add_difference_surface_and_pall(df, inplace=True):
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
    
    return new_df
