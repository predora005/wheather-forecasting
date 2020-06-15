# coding: utf-8

from .abs_loader import AbsLoader

import os
import pandas as pd
import gsm
import wfile
import wdfproc
from wdfproc import WeatherConvertMode

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
        gsm_df = self._load_gsm_weather(reload)
        print(gsm_df.info())
        
        # 地上気象データをロードする
        ground_df = self._load_ground_weather(reload)
        print(ground_df.info())
        
        # GSMデータと地上気象データをマージする
        df = pd.merge(gsm_df, ground_df, on=('日付','時'))
        print(df.info())
        df.to_csv('test.csv')
        
        return df
        
    ##################################################
    # GSMデータを読み込む
    ##################################################
    def _load_gsm_weather(self, reload):
        
        # GSMデータ(CSV)をロードする
        #gsm_df = gsm.load_gsm_csv(self._input_dir)
        #print(gsm_df.info())
        
        # 保存ファイルの有無を確認する
        os.makedirs(self._temp_dir, exist_ok=True)
        gsm_csv = os.path.join(self._temp_dir, 'gsm.csv')
        exist_csv = os.path.isfile(gsm_csv)
        
        if (reload == False) and (exist_csv == True):
            # 読み込み済み、かつ、リロード無しの場合は、
            # 保存したファイルを読み込む
            gsm_df = pd.read_csv(gsm_csv, index_col=0, parse_dates=[1])
        else:
            #ground_dir = os.path.join(self._input2_dir, 'ground_weather')
            #ground_df = wfile.get_ground_weather(ground_dir)
            gsm_df = gsm.load_gsm_csv(self._input_dir)
            gsm_df.to_csv(gsm_csv)
        
        # 不要な列を削る
        drop_columns = [
            '高度', '東西風', '南北風', '地上気圧', 
            '下層雲量', '中層雲量', '上層雲量',
            '積算降水量_06h', '積算降水量_12h', '積算降水量_24h'
        ]
        gsm_df = wdfproc.drop_columns(gsm_df, drop_columns)
        #print(gsm_df.info())
        
        return gsm_df
        
    ##################################################
    # 地上気象データを読み込む
    ##################################################
    def _load_ground_weather(self, reload):
        
        # 保存ファイルの有無を確認する
        os.makedirs(self._temp_dir, exist_ok=True)
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
        ground_df = util.extract_row_isin(ground_df, '時', [3, 9, 15, 21])
    
        # 天気を数値に変換する
        ground_df = wdfproc.convert_weather_to_interger(ground_df)
        #print(ground_df.info())
        
        # 天気を所定の境界値で分類する
        ground_df = wdfproc.replace_weather(ground_df, columns=['Mito_天気'])
        #ground_df = wdfproc.replace_weather(ground_df, columns=['Mito_天気'], mode=WeatherConvertMode.RainOrNot)
        
        # 水戸の天気,海面気圧,気温,湿度を抽出する
        extract_columns = ['日付', '時', 'Mito_海面気圧(hPa)', 'Mito_気温(℃)', 'Mito_湿度(％)', 'Mito_天気']
        ground_df = ground_df.loc[:, extract_columns]
        
        return ground_df
        
