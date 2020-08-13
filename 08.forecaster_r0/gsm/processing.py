# coding: utf-8

import numpy as np
import pandas as pd
import re
from metpy.units import units
import metpy.calc
#from metpy.calc import dewpoint_from_relative_humidity, equivalent_potential_temperature

##################################################
# GSMデータを指定した間隔で間引く
##################################################
def thin_out_gsm(df, interval=(2,2), inplace=True):
    """ GSMデータを指定した間隔で間引く
    
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
# GSMデータを指定した間隔で間引く。
# 間引く範囲の平均値で補間する。
##################################################
def thin_out_gsm_with_interpolation(df, interval=(4,4), inplace=True):
    """ GSMデータを指定した間隔で間引く
        間引く範囲の平均値で補間する。
    
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
    all_latitudes, all_longitudes = _get_latitudes_and_longitudes(new_df)
    
    # 残す緯度,経度を計算する
    base_latitudes = []
    for i in range(0, len(all_latitudes), interval[0]):
        base_latitudes.append(all_latitudes[i])
        
    base_longitudes = []
    for i in range(0, len(all_longitudes), interval[1]):
        base_longitudes.append(all_longitudes[i])
    
    # 指定した緯度,経度を含む列を抽出する
    remain_columns = ['日付', '時']         # 残す列のリスト
    num_latitudes = len(all_latitudes)      # 緯度の数
    num_longitudes = len(all_longitudes)    # 経度の数
    columns = new_df.columns                # データフレームの全列
    for column in new_df.columns:
        
        # 列名から地点名(Surf,300hPa等),緯度,経度,パラメータ名を抽出する
        result = re.search(r"(.*)_lat(\d+\.\d+)_long(\d+\.\d+)_(.*)", column)
        if result:
            spot = result.group(1)
            lati = result.group(2)
            longi = result.group(3)
            feature = result.group(4)
            
            # 残す緯度,経度のデータに間引くデータの平均値を代入する
            if (lati in base_latitudes) and (longi in base_longitudes):
                
                # 残す列のリストに列名を追加
                remain_columns.append(column)
                
                # インデックスの範囲を計算する
                lati_st = all_latitudes.index(lati)
                longi_st = all_longitudes.index(longi)
                lati_end = min(lati_st + interval[0], num_latitudes)
                longi_end = min(longi_st + interval[1], num_longitudes)
                
                # 指定した範囲の緯度,経度データの合計値を計算する
                sum_value = 0
                for i in range(lati_st, lati_end):
                    for j in range(longi_st, longi_end):
                        col = "{0:s}_lat{1:s}_long{2:s}_{3:s}".format(
                            spot, all_latitudes[i], all_longitudes[j], feature)
                        sum_value += new_df[col]
                
                # 平均値を残す列に代入する
                num = interval[0] * interval[1]
                new_df[column] = sum_value / num
        
    # 指定した列のみのDataFrameを作成する
    new_df = new_df[remain_columns]
    
    return new_df

##################################################
# 地表と指定気圧面の特徴量の差をDataFrameに追加する
##################################################
def add_difference_surface_and_pall(df, features, inplace=True):
    """ 地表と指定気圧面の特徴量の差をDataFrameに追加する

    Args:
        df(DataFrame)   : 変更対象のDataFrame
        features(list)  : 差を追加する特徴量のリスト
        inplace(bool)   : 元のDataFrameを変更するか否か

    Returns:
        DataFrame : 変更後のDataFrame
    """
    if inplace:
        new_df = df
    else:
        new_df = df.copy()
    
    # 緯度,経度,指定気圧面,特徴量のリストを取得
    latitudes, longitudes = _get_latitudes_and_longitudes(new_df)
    pressure_surfaces = _get_pressure_surfaces(new_df)
    all_features = _get_features(new_df)
    
    for latitude in latitudes:          # 緯度のループ
        for longitude in longitudes:    # 経度のループ
            for feature in all_features:    # 特徴量のループ
                
                # 指定した特徴量以外はcontinue
                if feature not in features:
                    continue
                
                # 地表の列名を作成
                surface_column = "Surf_lat{0:s}_long{1:s}_{2:s}".format(
                    latitude, longitude, feature)
                    
                # 指定した列名が含まれない場合はcontinue
                if not(surface_column  in new_df.columns):
                    continue
                
                for pressure_surface in pressure_surfaces:  # 指定気圧面のループ
                    
                    # 指定気圧面の列名を作成
                    psurface_column = "{0:s}hPa_lat{1:s}_long{2:s}_{3:s}".format(
                        pressure_surface, latitude, longitude, feature)
                    
                    # 新しい列名を作成
                    new_column = "{0:s}hPa-Surf_lat{1:s}_long{2:s}_{3:s}".format(
                        pressure_surface, latitude, longitude, feature)
                    
                    new_df[new_column] = new_df[psurface_column] - new_df[surface_column]
                
    return new_df

##################################################
# 指定気圧面の湿数をDataFrameに追加する
##################################################
def add_moisture(df, inplace=True):
    """ 指定気圧面の湿数をDataFrameに追加する

    Args:
        df(DataFrame) : 変更対象のDataFrame
        inplace(bool) : 元のDataFrameを変更するか否か

    Returns:
        DataFrame : 変更後のDataFrame
    """
    if inplace:
        new_df = df
    else:
        new_df = df.copy()
    
    # 緯度,経度,指定気圧面のリストを取得
    latitudes, longitudes = _get_latitudes_and_longitudes(new_df)
    pressure_surfaces = _get_pressure_surfaces(new_df)

    for latitude in latitudes:          # 緯度のループ
        for longitude in longitudes:    # 経度のループ
            
            for pressure_surface in pressure_surfaces:  # 指定気圧面のループ
                
                # 指定気圧面の気温と湿度を取得する
                temperature = "{0:s}hPa_lat{1:s}_long{2:s}_気温".format(
                    pressure_surface, latitude, longitude)
                humidity= "{0:s}hPa_lat{1:s}_long{2:s}_相対湿度".format(
                    pressure_surface, latitude, longitude)
                
                # 露点温度を計算する
                dewpoint = metpy.calc.dewpoint_from_relative_humidity(
                    new_df[temperature].values * units('K'),
                    new_df[humidity].values / 100.
                ).to(units('K'))
                
                # 湿数の列を追加する
                moisture = "{0:s}hPa_lat{1:s}_long{2:s}_湿数".format(
                    pressure_surface, latitude, longitude)
                
                # 湿数 = 気温 - 露点温度
                new_df[moisture] = new_df[temperature] - dewpoint.magnitude
            
    return new_df

##################################################
# 指定気圧面の相当温位をDataFrameに追加する
##################################################
def add_potential_temperature(df, inplace=True):
    """ 指定気圧面の相当温位をDataFrameに追加する

    Args:
        df(DataFrame) : 変更対象のDataFrame
        inplace(bool) : 元のDataFrameを変更するか否か

    Returns:
        DataFrame : 変更後のDataFrame
    """
    if inplace:
        new_df = df
    else:
        new_df = df.copy()
    
    # 緯度,経度,指定気圧面のリストを取得
    latitudes, longitudes = _get_latitudes_and_longitudes(new_df)
    pressure_surfaces = _get_pressure_surfaces(new_df)

    for latitude in latitudes:          # 緯度のループ
        for longitude in longitudes:    # 経度のループ
            
            ##################################################
            # 指定気圧面の相当温位をDataFrameに追加する
            for pressure_surface in pressure_surfaces:  # 指定気圧面のループ
                
                # 計算用に気圧のndarrayを用意する
                pressure = np.full(new_df.shape[0], float(pressure_surface))
                
                # 指定気圧面の気温,相対湿度を取得する
                temperature = "{0:s}hPa_lat{1:s}_long{2:s}_気温".format(
                    pressure_surface, latitude, longitude)
                humidity= "{0:s}hPa_lat{1:s}_long{2:s}_相対湿度".format(
                    pressure_surface, latitude, longitude)

                # 露点温度を計算する
                dewpoint = metpy.calc.dewpoint_from_relative_humidity(
                    new_df[temperature].values * units('K'),
                    new_df[humidity].values / 100.
                ).to(units('K'))
                
                # 相当温位を計算する
                potensial_temperature = metpy.calc.equivalent_potential_temperature(
                        pressure * units('hPa'),
                        new_df[temperature].values * units('K'),
                        dewpoint
                )
                
                # 相当温位の列を追加する
                pt = "{0:s}hPa_lat{1:s}_long{2:s}_相当温位".format(
                    pressure_surface, latitude, longitude)
                new_df[pt] = potensial_temperature.magnitude
            
            ##################################################
            # 地上の相当温位をDataFrameに追加する
            
            # 気温,相対湿度,地上気圧を取得する
            temperature = "Surf_lat{0:s}_long{1:s}_気温".format(latitude, longitude)
            humidity= "Surf_lat{0:s}_long{1:s}_相対湿度".format(latitude, longitude)
            pressure = "Surf_lat{0:s}_long{1:s}_地上気圧".format(latitude, longitude)

            # 露点温度を計算する
            dewpoint = metpy.calc.dewpoint_from_relative_humidity(
                new_df[temperature].values * units('K'),
                new_df[humidity].values / 100.
            ).to(units('K'))
            
            # 相当温位を計算する
            potensial_temperature = metpy.calc.equivalent_potential_temperature(
                    new_df[pressure].values / 100 * units('hPa'),
                    new_df[temperature].values * units('K'),
                    dewpoint
            )
            
            # 相当温位の列を追加する
            pt = "Surf_lat{0:s}_long{1:s}_相当温位".format(latitude, longitude)
            new_df[pt] = potensial_temperature.magnitude
    
    return new_df

##################################################
# 指定した範囲の緯度,経度のデータを抽出する
##################################################
def extract_latitude_and_longitude(df, latitudes, longitudes, inplace=True):
    """ 指定した緯度,経度のデータを抽出する

    Args:
        df(DataFrame)       : 変更対象のDataFrame
        latitudes(tuple)    : 緯度の範囲
        longitudes(tuple)   : 経度の範囲
        inplace(bool)       : 元のDataFrameを変更するか否か

    Returns:
        DataFrame : 変更後のDataFrame
    """
    if inplace:
        new_df = df
    else:
        new_df = df.copy()
    
    # 緯度,経度を取り出す
    st_lat = latitudes[0]
    ed_lat = latitudes[1]
    st_long = longitudes[0]
    ed_long = longitudes[1]
    
    # 列名のリストを用意する
    new_columns = ['日付', '時']
    
    for column in df.columns:
        
        # 地表データを抽出する
        #   (ex)'Surf_lat38.00_long135.000_海面更正気圧'
        result = re.search(r"Surf_lat(\d+\.\d+)_long(\d+\.\d+)_(.*)", column)
        if result:
            latitude = float(result.group(1))
            longitude = float(result.group(2))
            
            # 指定した緯度,経度のデータであれば、列をリストに格納する
            if (st_lat <= latitude) and (latitude <= ed_lat):
                if (st_long <= longitude) and (longitude <= ed_long):
                    new_columns.append(column)
            
        # 指定気圧面データを抽出する
        #   (ex)'850hPa_lat38.00_long135.000_気温'
        result = re.search(r"(\d+)hPa_lat(\d+\.\d+)_long(\d+\.\d+)_(.*)", column)
        if result:
            latitude = float(result.group(2))
            longitude = float(result.group(3))
            
            # 指定した緯度,経度のデータであれば、列をリストに格納する
            if (st_lat <= latitude) and (latitude <= ed_lat):
                if (st_long <= longitude) and (longitude <= ed_long):
                    new_columns.append(column)
            
    # 指定した列のみのDataFrameを作成する
    new_df = new_df[new_columns]
    
    return new_df
    
##################################################
# 指定気圧面のジオポテンシャル高度偏差をDataFrameに追加する
##################################################
def add_height_diviation(df, inplace=True):
    """ 指定気圧面のジオポテンシャル高度偏差をDataFrameに追加する

    Args:
        df(DataFrame) : 変更対象のDataFrame
        inplace(bool) : 元のDataFrameを変更するか否か

    Returns:
        DataFrame : 変更後のDataFrame
    """
    if inplace:
        new_df = df
    else:
        new_df = df.copy()
    
    # 緯度,経度,指定気圧面のリストを取得
    latitudes, longitudes = _get_latitudes_and_longitudes(new_df)
    pressure_surfaces = _get_pressure_surfaces(new_df)
    
    num_height = len(latitudes) * len(longitudes)
    for pressure_surface in pressure_surfaces:  # 指定気圧面のループ
        
        mean_height = 0
        for latitude in latitudes:          # 緯度のループ
            for longitude in longitudes:    # 経度のループ
                
                # 指定気圧面のジオポテンシャル高度を取得する
                height = "{0:s}hPa_lat{1:s}_long{2:s}_高度".format(
                    pressure_surface, latitude, longitude)
                    
                mean_height += new_df[height] / float(num_height)
        
        # 高度偏差の列を追加する
        for latitude in latitudes:          # 緯度のループ
            for longitude in longitudes:    # 経度のループ
            
                height = "{0:s}hPa_lat{1:s}_long{2:s}_高度".format(
                    pressure_surface, latitude, longitude)
                
                height_diviation = "{0:s}hPa_lat{1:s}_long{2:s}_高度偏差".format(
                    pressure_surface, latitude, longitude)
                
                new_df[height_diviation] = new_df[height] - mean_height
    
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
