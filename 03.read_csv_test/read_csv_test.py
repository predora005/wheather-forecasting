# coding: utf-8

import os
import pandas as pd
import wcsv
import wdfproc
import re
#from wcsv import *
#from wdfproc import *

##################################################
# 地上の気象データ取得
##################################################
def get_ground_weather(dir_path):
    
    # 地上気象データのファイル一覧取得
    file_paths = wcsv.get_file_paths(dir_path)

    # 気象データを読み込み、DataFrameに格納する
    weather_df = None
    for file_path in file_paths:
        
        # 地上気象データ読み込み
        df = wcsv.read_ground(file_path)
        #print(df.head())
    
        # 指定した列のデータを抽出
        #columns = [ ('時','時'), ('湿度(％)','湿度(％)'), ('天気','天気') ]
        #df1 = wdfproc.extract_from_columns(df, columns)
        #print(df1.head())
        
        #df1.columns = [t1 for t1, t2 in df1.columns]
        #print(df1.head())
        
        # 指定した行のデータを抽出
        df1 = wdfproc.extract_row_isin(df, ('時', '時'), [9, 21])
        
        # DataFrameに追加する
        if weather_df is None:
            weather_df = df1
        else:
            weather_df = weather_df.append(df1)
    
    # 地点名を取得する
    dirname = os.path.basename(dir_path)
    elements = wcsv.elements_from_dirname(dirname)
    place_name = elements['place_name']

    # 列名を変更する
    weather_df = wdfproc.rename_column_ground(weather_df, place_name)
    
    return weather_df
    
##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    # 地上の気象データが格納されたディレクトリの一覧を取得する
    cwd = os.getcwd()
    input_dir = cwd + '/' + 'ground_weather'
    dirs = os.listdir(input_dir)
    
    weather_df = None
    for dir_name in dirs:
        
        dir_path = os.path.join(input_dir, dir_name)
        
        df = get_ground_weather(dir_path)
        
        if weather_df is None:
            weather_df = df
        else:
            weather_df = pd.merge(weather_df, df, on=('日付','時'))
    
    print(weather_df.head())
    weather_df.to_csv('test.csv')