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
    """ 1地点の地上気象データを取得する
    
    Args:
        dir_path(string) : ディレクトリパス

    Returns:
        DataFrame : ファイルの読込結果
    """
    
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
    """ 複数地点の地上気象データを取得する
    
    Args:
        input_dir(string) : ディレクトリパス

    Returns:
        DataFrame : ファイルの読込結果
    """
    
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
    
    # 日付と時の列を先頭に移動する
    ground_df = move_datetime_column_to_top(ground_df)
    
    #new_columns = ['日付', '時']
    #for col in ground_df.columns:
    #    if (col != '日付') and (col != '時'):
    #        new_columns.append(col)
    #
    #ground_df = ground_df.loc[:, new_columns]
    
    return ground_df
    
    
##################################################
# 1地点の高層気象データを取得する
##################################################
def get_highrise_weather_one_place(dir_path, boundary_pressure=350):
    """ 1地点の高層気象データを取得する
    
    Args:
        dir_path(string)            : ディレクトリパス
        boundary_pressure(float)    : 指定した気圧(hPa)より大きい指定気圧面のデータを扱う

    Returns:
        DataFrame : ファイルの読込結果
    """
    
    # 高層気象データのファイル一覧取得
    file_paths = read_csv.get_file_paths(dir_path)

    # 気象データを読み込み、DataFrameに格納する
    highrise_df = None
    for file_path in file_paths:
            
        # 高層気象データ読み込み
        df = read_csv.read_highrise(file_path)
        
        #if file_path == '/home/ec2-user/highrise_weather/Shionomisaki_47778/Shionomisaki_47778_2017_01_30_H21.csv':
        #    print(df)
            
        # 指定した気圧(hPa)より大きい指定気圧面のデータを抽出する
        df = df[df['気圧(hPa)'] > boundary_pressure]

        #if file_path == '/home/ec2-user/highrise_weather/Shionomisaki_47778/Shionomisaki_47778_2017_01_30_H21.csv':
        #    print(df)
            
        # 日付と時刻データを抽出する
        date = df.loc[1,'日付']
        hour = df.loc[1,'時']

        # 新しい列名のPrefixを作成する
        new_column_prefix = []
        new_column_prefix.append('地上_')
        for i in range(1, len(df)):
            prefix = '{0:.0f}hPa_'.format(df.loc[i,'気圧(hPa)'])
            new_column_prefix.append(prefix)
                
        # 新しい列名を作成する
        #   ex) 1000hPa_高度(m)
        new_columns = []
        for col in df.columns:
            # '日付','時', '気圧(hPa)'を除いた列を扱う
            if col not in ('日付', '時', '気圧(hPa)'):
                for prefix in new_column_prefix:
                    new_column = prefix + col
                    new_columns.append(new_column)
        
        # 複数列のデータを1列のデータに展開する
        new_values = []
        for col in df.columns:
            if col not in ('日付', '時', '気圧(hPa)'):
                new_values.extend(df[col].tolist())
        
        # 新しいDataFrameを作成する
        df = pd.DataFrame(new_values, index=new_columns)
        
        # 1列のDataFrameから1行のDataFrameに変換する
        df = df.T
        
        # 日付と時刻をDataFrameに追加する
        df['日付'] = date
        df['時'] = hour

        # DataFrameに追加する
        if highrise_df is None:
            highrise_df = df
        else:
            highrise_df = highrise_df.append(df)
    
    # 地点名を取得する
    dirname = os.path.basename(dir_path)
    elements = name_handle.elements_from_dirname_highrise(dirname)
    place_name = elements['name']

    # 列名を変更する
    highrise_df = wdfproc.rename_column_highrise(highrise_df, place_name)
    
    return highrise_df
    
##################################################
# 複数地点の高層気象データを取得する
##################################################
def get_highrise_weather(input_dir):
    """ 複数地点の高層気象データを取得する
    
    Args:
        input_dir(string) : ディレクトリパス

    Returns:
        DataFrame : ファイルの読込結果
    """
    
    # 高層の気象データが格納されたディレクトリの一覧を取得し、
    # 順番にDataFrameに格納していく
    highrise_df = None
    for dir_name in os.listdir(input_dir):
        
        # 1地点の高層気象データを取得する
        dir_path = os.path.join(input_dir, dir_name)
        df = get_highrise_weather_one_place(dir_path)
        
        # 気象データを結合する
        if highrise_df is None:
            highrise_df = df
        else:
            highrise_df = pd.merge(highrise_df, df, on=('日付','時'))
    
    # 日付と時の列を先頭に移動する
    highrise_df = move_datetime_column_to_top(highrise_df)
    
    return highrise_df
    
##################################################
# 日付・時刻の列を先頭に移動する
##################################################
def move_datetime_column_to_top(df):
    """ 日付・時刻の列を先頭に移動する

    Args:
        df(DataFrame) : 変換対象のDataFrame

    Returns:
        DataFrame : 変換後のDataFrame
    """
    new_columns = ['日付', '時']
    for col in df.columns:
        if (col != '日付') and (col != '時'):
            new_columns.append(col)
    
    new_df = df.loc[:, new_columns]
    
    return new_df
