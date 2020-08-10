# coding: utf-8

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import util
from loader import GsmLoader2020Ver1

##################################################
# GSMデータの分析クラス
# 2020 Ver1。
# 改善前の初期状態。
##################################################
class GsmDataAnalyzer2020Ver1:
    """ GSMデータの分析クラス

    Attributes:
        params (dict)       : パラメータ
    """
    
    ##################################################
    # コンストラクタ
    ##################################################
    def __init__(self, params):
        
        self._params = params
        
        # ディレクトリ名
        self._base_dir = self._params['base_dir']
        self._temp_dir = self._params['temp_dir']
        self._input_dir = self._params['input_dir']
        self._input2_dir = self._params['input2_dir']
        self._output_dir = self._params['output_dir']
        
        # GSMデータを間引く間隔
        self._gsm_thinout_interval = self._params['gsm_thinout_interval']
        
        # 天気を変換する際のモード
        self._weather_convert_mode = self._params['weather_convert_mode']
        
        # クラス名
        self._class_names = self._params['class_names']
        self._label_name = self._params['label_name']
        
        # データ読み込み済みフラグ
        self._is_data_loaded = False
        
    ##################################################
    # 分析を実行する
    ##################################################
    def run(self):
        
        # データをロードする
        load_data = self._load_data()
        
        # 積算降水量と水戸-天気の関係を可視化する
        self._visualize_total_precipitation_and_weather(load_data)
        
        
    ##################################################
    # 積算降水量と水戸-天気の関係を可視化する
    ##################################################
    def _visualize_total_precipitation_and_weather(self, data):
        
        #total_precipitation_24h = data['Surf_lat36.00_long140.000_積算降水量_24h']
        total_precipitation_24h = data['Surf_lat35.60_long140.000_積算降水量_24h']
        mito_weather = data[self._label_name]
        mito_weather = mito_weather.replace({0: '晴れ', 1: 'くもり', 2: '雨'})
        df = pd.DataFrame( {
            '積算降水量_24h': total_precipitation_24h, 
            '水戸_天気': mito_weather
        } )
        df.to_csv('test.csv')
        
        grid = sns.FacetGrid(df, hue='水戸_天気', aspect=2)
        grid.map(sns.kdeplot, '積算降水量_24h', shade=True)
        max_value = total_precipitation_24h.max()
        grid.set(xlim=(0, 20))
        grid.add_legend()
        grid.savefig('kdeplot.png')
        
        bins = np.arange(0, 20, 2)
        grid = sns.FacetGrid(df, col='水戸_天気', height=5)
        grid.map(plt.hist, '積算降水量_24h', bins=bins)
        grid.add_legend()
        grid.savefig('hist.png')
        
    ##################################################
    # 学習・評価・予測用のデータをロードする
    ##################################################
    def _load_data(self):
        
        # データ未読み込みの場合
        if self._is_data_loaded == False:
        
            # 気象データを読み込み
            loader = GsmLoader2020Ver1(
                self._base_dir, self._temp_dir, self._input_dir, self._label_name,
                self._input2_dir, self._gsm_thinout_interval, self._weather_convert_mode)
            df = loader.load()
            
            # 読み込んだデータをクラス変数に保存
            self._load_data = df
            
            # 読み込み済みフラグON
            self._is_data_loaded = True
            
        return self._load_data 