# coding: utf-8

import sys
sys.path.append('../')
import util
import wdfproc

import os
import pandas as pd

##################################################
# GSMデータのCSVファイルを読み込む
##################################################
def load_gsm_csv(input_dir):
    
    # 指定したディレクリ下のディレクトリの一覧を取得し、
    # 順番にDataFrameに格納していく
    gsm_df = None
    for dir_name in os.listdir(input_dir):
        
        # 1ディレクトリ内のGSMデータを取得する
        dir_path = os.path.join(input_dir, dir_name)
        df = load_gsm_csv_one_dir(dir_path)
        
        # DataFrameを結合する
        if gsm_df is None:
            gsm_df = df
        else:
            gsm_df = pd.merge(gsm_df, df, on=('日付','時'))
    
    # 日付と時の列を先頭に移動する
    #gsm_df = util.move_datetime_column_to_top(gsm_df)
    
    return gsm_df
    
##################################################
# 指定したディレクトリに格納されている
# GSMデータのCSVファイルを読み込む
##################################################
def load_gsm_csv_one_dir(dir_path):
    """ GSMデータのCSVファイルを読み込む
    
    Args:
        dir_path(string) : ディレクトリパス

    Returns:
        DataFrame : ファイルの読込結果
    """
    
    # 指定ディレクトリのCSVファイル一覧取得
    file_paths = util.get_file_paths(dir_path, '.csv')
    
    # 退避用のリスト作成
    gsm_df_list = []
    
    # GSMデータを読み込み、DataFrameに格納する
    gsm_df = None
    for file_path in file_paths:
        
        # CSVファイル読み込み
        df = pd.read_csv(file_path, sep=',', skiprows=0, header=0, index_col=0, parse_dates=[1])
        
        # DataFrameに追加する
        if gsm_df is None:
            gsm_df = df
        else:
            gsm_df = gsm_df.append(df)
        
        # DataFrameに一定の行数データが溜まったらリストに退避する
        if len(gsm_df) > 256:
            gsm_df_list.append(gsm_df)
            gsm_df = None
    
    # リストに溜まったDataFrameを結合する
    if len(gsm_df_list) > 0:
        
        # リスト内のDataFrameを結合する
        list_df = gsm_df_list[0].copy()
        for i in range(1, len(gsm_df_list)):
            list_df = list_df.append(gsm_df_list[i])
    
        # リストに登録していないDataFrameを結合する
        if gsm_df is not None:
            list_df = list_df.append(gsm_df)
            
        gsm_df = list_df
    
    return gsm_df
    
##################################################
# GSMデータのpickleファイルを読み込む
##################################################
def load_gsm_pickle(input_dir):
    
    # 指定したディレクリ下のディレクトリの一覧を取得し、
    # 順番にDataFrameに格納していく
    gsm_df = None
    for dir_name in os.listdir(input_dir):
        
        # 1ディレクトリ内のGSMデータを取得する
        dir_path = os.path.join(input_dir, dir_name)
        df = load_gsm_pickle_one_dir(dir_path)

        # DataFrameを結合する
        if gsm_df is None:
            gsm_df = df
        else:
            gsm_df = pd.merge(gsm_df, df, on=('日付','時'))
    
    # 日付と時の列を先頭に移動する
    #gsm_df = util.move_datetime_column_to_top(gsm_df)
    
    return gsm_df

##################################################
# 指定したディレクトリに格納されている
# GSMデータのpickleファイルを読み込む
##################################################
def load_gsm_pickle_one_dir(dir_path):
    """ GSMデータのpickleファイルを読み込む
    
    Args:
        dir_path(string) : ディレクトリパス

    Returns:
        DataFrame : ファイルの読込結果
    """
    
    # 指定ディレクトリのpickleファイル一覧取得
    file_paths = util.get_file_paths(dir_path, '.pickle')
    
    # 退避用のリスト作成
    gsm_df_list = []
    
    # GSMデータを読み込み、DataFrameに格納する
    gsm_df = None
    for file_path in file_paths:
        
        # pickleファイル読み込み
        #df = pd.read_csv(file_path, sep=',', skiprows=0, header=0, index_col=0, parse_dates=[1])
        df = pd.read_pickle(file_path)
        
        # DataFrameに追加する
        if gsm_df is None:
            gsm_df = df
        else:
            gsm_df = gsm_df.append(df)
        
        # DataFrameに一定の行数データが溜まったらリストに退避する
        if len(gsm_df) > 256:
            gsm_df_list.append(gsm_df)
            gsm_df = None
    
    # リストに溜まったDataFrameを結合する
    if len(gsm_df_list) > 0:
        
        # リスト内のDataFrameを結合する
        list_df = gsm_df_list[0].copy()
        for i in range(1, len(gsm_df_list)):
            list_df = list_df.append(gsm_df_list[i])
    
        # リストに登録していないDataFrameを結合する
        if gsm_df is not None:
            list_df = list_df.append(gsm_df)
            
        gsm_df = list_df
    
    return gsm_df
    
