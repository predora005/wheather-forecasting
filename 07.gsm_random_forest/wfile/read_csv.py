# coding: utf-8

import os
import pandas as pd
import re
import datetime
from . import name_handle

##################################################
# CSVファイルから地上の気象データを読み込み、
# DataFrameを返す
##################################################
def read_ground(file_path):
    """ CSVファイルから地上の気象データを読み込み、
        DataFrameを返す
    
    Args:
        file_path    (string) : ファイルパス

    Returns:
        DataFrame : ファイルの読込結果
    """
    
    # CSVファイル読み込み
    df = pd.read_csv(file_path, sep=',', skiprows=0, header=[0,1], index_col=0)
    
    # ファイル名から地点名、日付を抽出
    file_name = os.path.basename(file_path)
    elements = name_handle.elements_from_filename_ground(file_name)
    name = elements['name']
    year = elements['year']
    month = elements['month']
    day = elements['day']

    # 日付をDataFrameに追加する
    date = datetime.datetime(year, month, day)
    df[('日付','日付')] = date
    
    # 地点名をDataFrameに追加する
    #df[('地点','地点')] = name
    
    return df

##################################################
# CSVファイルから高層の気象データを読み込み、
# DataFrameを返す
##################################################
def read_highrise(file_path):
    """ CSVファイルから高層の気象データを読み込み、
        DataFrameを返す
    
    Args:
        file_path    (string) : ファイルパス

    Returns:
        DataFrame : ファイルの読込結果
    """
    
    # CSVファイル読み込み
    df = pd.read_csv(file_path, sep=',', skiprows=0, header=[0], index_col=0)
    
    # ファイル名から地点名、日付を抽出
    file_name = os.path.basename(file_path)
    elements = name_handle.elements_from_filename_highrise(file_name)
    name = elements['name']
    year = elements['year']
    month = elements['month']
    day = elements['day']
    hour = elements['hour']

    # 日付をDataFrameに追加する
    date = datetime.datetime(year, month, day)
    df['日付'] = date
    
    # 時刻をDataFrameに追加する
    df['時'] = hour
    
    # 地点名をDataFrameに追加する
    #df['地点'] = name
    
    return df

