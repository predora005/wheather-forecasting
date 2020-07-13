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
    
    # 緯度,経度,指定気圧面,特徴量のリストを取得
    latitudes, longitudes = _get_latitudes_and_longitudes(new_df)
    pressure_surfaces = _get_pressure_surfaces(new_df)
    features = _get_features(new_df)
    print(latitudes)
    print(longitudes)
    print(pressure_surfaces)
    print(features)
    
    for latitude in latitudes:          # 緯度のループ
        for longitude in longitudes:    # 経度のループ
            for feature in features:    # 特徴量のループ
                
                # 地表の列名を作成
                surface_column = "Surf_lat{0:s}_long{1:s}_{2:s}".format(
                    latitude, longitude, feature)
                    
                print(surface_column)
                    
                # 指定した列名が含まれない場合はcontinue
                if not(surface_column  in new_df.columns):
                    continue
                
                for pressure_surface in pressure_surfaces:  # 指定気圧面のループ
                    
                    # 指定気圧面の列名を作成
                    psurface_column = "{0:s}_lat{1:s}_long{2:s}_{3:s}".format(
                        pressure_surface, latitude, longitude, feature)
                    
                    # 新しい列名を作成
                    new_column = "{0:s}-Surf_lat{1:s}_long{2:s}_{3:s}".format(
                        pressure_surface, latitude, longitude, feature)
                    
                    print(surface_column, psurface_column, new_column)
                
                    new_df[new_column] = new_df[psurface_column] - new_df[surface_column]
                
    return new_df

##################################################
# 緯度と経度の一覧を取得する
##################################################
def _get_latitudes_and_longitudes(df):
    """ 緯度と経度の一覧を取得する
    
    Args:
        df(DataFrame) : DataFrame
    
    Returns:
        latitudes   : 緯度のリスト
        longitudes  : 経度のリスト
    """
    
    # 列名から緯度,経度を抽出する
    latitudes = []
    longitudes = []
    for column in df.columns:
        # 'Surf_lat38.00_long135.000_海面更正気圧'
        result = re.search(r"Surf_lat(\d+\.\d+)_long(\d+\.\d+)_(.*)", column)
        if result:
            latitude = result.group(1)
            longitude = result.group(2)
    
            # 緯度を追加
            if latitude not in latitudes:
                latitudes.append(latitude)
            
            # 経度を追加
            if longitude not in longitudes:
                longitudes.append(longitude)
    
    return latitudes, longitudes

##################################################
# 指定気圧面の一覧を取得する
##################################################
def _get_pressure_surfaces(df):
    """ 指定気圧面の一覧を取得する
    
    Args:
        df(DataFrame) : DataFrame
    
    Returns:
        pressure_surfaces   : 指定気圧面のリスト
    """
    
    # 列名から指定気圧面を抽出する
    pressure_surfaces = []
    for column in df.columns:
        # '850hPa_lat38.00_long135.000_気温'
        result = re.search(r"(\d+)hPa_lat(\d+\.\d+)_long(\d+\.\d+)_(.*)", column)
        if result:
            pressure_surface = result.group(1)
            
            # リストに追加
            if pressure_surface not in pressure_surfaces:
                pressure_surfaces.append(pressure_surface)
            
    return pressure_surfaces

##################################################
# 特徴量の一覧を取得する
##################################################
def _get_features(df):
    """ 特徴量の一覧を取得する
    
    Args:
        df(DataFrame) : DataFrame
    
    Returns:
        features    : 特徴量のリスト
    """
    
    # 列名から指定気圧面を抽出する
    features = []
    for column in df.columns:
        # '850hPa_lat38.00_long135.000_気温'
        result = re.search(r"(\d+)hPa_lat(\d+\.\d+)_long(\d+\.\d+)_(.*)", column)
        if result:
            feature = result.group(4)
            
            # リストに追加
            if feature not in features:
                features.append(feature)
            
    return features
