# coding: utf-8

from .abs_loader import AbsLoader

import os
import pandas as pd
import gsm
import wfile
import wdfproc

##################################################
# GSMデータロードクラス
##################################################
class GsmLoader(AbsLoader):
    """データロードクラス
        
    Attributes:
        _base_dir (string)      : ベースディレクトリ
        _temp_dirname (string)  : 一時ディレクトリ名
        _input_dirname (string) : 入力ディレクトリ名
    """
    
    ##################################################
    # コンストラクタ
    ##################################################
    def __init__(self, base_dir, temp_dirname, input_dirname, input2_dirname):
        
        # 抽象クラスのコンストラクタ
        super().__init__(base_dir, temp_dirname, input_dirname)
        
        self._input2_dirname = input2_dirname
        self._input2_dir = os.path.join(self._base_dir, self._input2_dirname)
        
    ##################################################
    # データをロードする
    ##################################################
    def load(self, reload=False):
        
        # GSMデータをロードする
        gsm_df = gsm.load_gsm_csv(self._input_dir)
        print(gsm_df.info())
        
        # 地上気象データをロードする
        groun_df = self._load_ground_weather(reload)
        print(groun_df.info())
        
        # GSMデータと地上気象データをマージする
        df = pd.merge(gsm_df, groun_df, on=('日付','時'))
        print(df.info())
        df.to_csv('test.csv')
        
        return df
        
    ##################################################
    # 地上気象データを読み込む
    ##################################################
    def _load_ground_weather(self, reload):
        
        # 保存ファイルの有無を確認する
        ground_weather_csv = os.path.join(self._temp_dir, 'ground_weather.csv')
        exist_csv = os.path.isfile(ground_weather_csv)
        
        if (reload == False) and (exist_csv == True):
            # 読み込み済み、かつ、リロード無しの場合は、
            # 保存したファイルを読み込む
            ground_df = pd.read_csv(ground_weather_csv, index_col=0, parse_dates=[1])
        else:
            ground_dir = os.path.join(self._input2_dir, 'ground_weather')
            ground_df = wfile.get_ground_weather(ground_dir)
            ground_df.to_csv(ground_weather_csv)
        
        # 3時,9時,15時,21時のデータを抽出する
        ground_df = wdfproc.extract_row_isin(ground_df, '時', [3, 9, 15, 21])
    
        # 天気を数値に変換する
        ground_df = wdfproc.convert_weather_to_interger(ground_df)
        
        # 天気を所定の境界値で分類する
        ground_df = wdfproc.replace_weather(ground_df, columns=['Mito_天気'])
        
        # 水戸の天気を抽出する
        ground_df = ground_df.loc[:, ['日付', '時', 'Mito_天気']]
        
        return ground_df
        
