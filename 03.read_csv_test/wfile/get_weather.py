# coding: utf-8

import sys
sys.path.append('../')
import wdfproc

import os
import pandas as pd
from . import read_csv
from . import name_handle

##################################################
# 1地点の地上気象データを取得する
##################################################
def get_ground_weather_one_place(dir_path):
    
    # 地上気象データのファイル一覧取得
    file_paths = read_csv.get_file_paths(dir_path)

    # 気象データを読み込み、DataFrameに格納する
    ground_df = None
    for file_path in file_paths:
        
        # 地上気象データ読み込み
        df = read_csv.read_ground(file_path)

        # 指定した行のデータを抽出
        df1 = wdfproc.extract_row_isin(df, ('時', '時'), [9, 21])
        
        # DataFrameに追加する
        if ground_df is None:
            ground_df = df1
        else:
            ground_df = ground_df.append(df1)
    
    # 地点名を取得する
    dirname = os.path.basename(dir_path)
    elements = name_handle.elements_from_dirname_ground(dirname)
    place_name = elements['name']

    # 列名を変更する
    ground_df = wdfproc.rename_column_ground(ground_df, place_name)
    
    return ground_df
    
##################################################
# 複数地点の地上気象データを取得する
##################################################
def get_ground_weather(input_dir):
    
    # 地上の気象データが格納されたディレクトリの一覧を取得し、
    # 順番にDataFrameに格納していく
    ground_df = None
    for dir_name in os.listdir(input_dir):
        
        # 1地点の地上気象データを取得する
        dir_path = os.path.join(input_dir, dir_name)
        df = get_ground_weather_one_place(dir_path)
        
        # 気象データを結合する
        if ground_df is None:
            ground_df = df
        else:
            ground_df = pd.merge(ground_df, df, on=('日付','時'))
    
    return ground_df