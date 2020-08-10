# coding: utf-8

from .abs_loader import AbsLoader

import os
import pandas as pd
import wfile
import wdfproc
import util

##################################################
# 地上気象観測データロードクラス。
# 2019年モデル。
##################################################
class Loader2019(AbsLoader):
    """データロードクラス
        
    Attributes:
        _base_dir (string)      : ベースディレクトリ
        _temp_dirname (string)  : 一時ディレクトリ名
        _input_dirname (string) : 入力ディレクトリ名
        _label_name (string)    : 正解データのラベル名
    """
    
    ##################################################
    # コンストラクタ
    ##################################################
    def __init__(self, base_dir, temp_dirname, input_dirname, label_name):
        
        # 抽象クラスのコンストラクタ
        super().__init__(base_dir, temp_dirname, input_dirname, label_name)
        
    ##################################################
    # データをロードする
    ##################################################
    def load(self, reload=False):
        
        # ワーク用ディレクトリを作成する
        os.makedirs(self._temp_dir, exist_ok=True)

        # 地上気象データを取得する
        gdf = self._load_ground_weather(reload)
        
        # 地上気象データに前処理を施す
        gdf = self._preprocess_ground_weather(gdf)
        
        return gdf
        
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
            ground_dir = os.path.join(self._input_dir, 'ground_weather')
            ground_df = wfile.get_ground_weather(ground_dir)
            ground_df.to_csv(ground_weather_csv)
        
        return ground_df
        
    ##################################################
    # 地上気象データに前処理を施す
    ##################################################
    def _preprocess_ground_weather(self, ground_df):
        
        # 9時と21時のデータを抽出する
        ground_df = util.extract_row_isin(ground_df, '時', [3, 9, 15, 21])
        
        # 天気記号を数値に変換する
        ground_df = wdfproc.convert_symbol_to_number(ground_df)
        
        # 地上気象データから不要データを除去する
        ground_df = wdfproc.drop_unneeded_ground(ground_df)

        # 風速・風向きを数値に変換する
        ground_df = wdfproc.convert_wind_to_vector_ground(ground_df)

        # 天気を数値に変換する
        ground_df = wdfproc.convert_weather_to_interger(ground_df)

        # 雲量を浮動小数点数に変換する
        ground_df = wdfproc.convert_cloud_volume_to_float(ground_df)

        # 天気を晴れ,くもり,雨のいずれかに分類する
        weather_cols = [col for col in ground_df.columns if('天気' in col)]
        ground_df = wdfproc.replace_weather(
                            ground_df, columns=weather_cols, 
                             mode=wdfproc.WeatherConvertMode.Coarse)
        
        # 浮動小数点数を32ビットに変換する
        ground_df = util.type_to_float32(ground_df)

        # 不要な列を除去する(正解データは除く)
        ground_df = wdfproc.drop_columns(
            ground_df, 
            [ '現地気圧', '露点温度', '蒸気圧', '風速', '日照時間', '全天日射', 
              '降雪', '積雪', '雲量', '視程']
        )
        weather_cols.pop( weather_cols.index(self._label_name) )
        ground_df = ground_df.drop(columns=weather_cols)
        
        print(ground_df.info())
        
        return ground_df

