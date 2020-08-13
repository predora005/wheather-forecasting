# coding: utf-8

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

from loader import GsmLoader2020Ver3

##################################################
# GSMデータの分析クラス
# 2020 Ver3。
# 改善後。
##################################################
class GsmDataAnalyzer2020Ver3:
    """ GSMデータの分析クラス

    Attributes:
        params (dict)       : パラメータ
    """
    
    ##################################################
    # コンストラクタ
    ##################################################
    def __init__(self, run_name, params):
        
        self._params = params
        self._run_name = run_name
        
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
        
        # データを特徴量とラベルに分け、学習時と同様のデータを作る
        features, label = self._make_training_data(load_data)
        
        # 解析用の列を追加する
        features = self._add_columns_for_analysis(features)
        
        # 出力ディレクトリを作成する
        output_dirpath = os.path.join(self._base_dir, self._output_dir, self._run_name)
        os.makedirs(output_dirpath, exist_ok=True)
        
        sns.set_palette('muted')
        
        # 湿数と水戸-天気の関係を可視化する
        self._visualize_moisture_and_weather(features, label, output_dirpath)
        
        # 相当温位と水戸-天気の関係を可視化する
        self._visualize_potential_temperature_and_weather(features, label, output_dirpath)
        
    ##################################################
    # 湿数と水戸-天気の関係を可視化する
    ##################################################
    def _visualize_moisture_and_weather(self, features, lebel_data, output_dirpath):
        
        moisture_dirpath = os.path.join(output_dirpath, 'moisture')
        os.makedirs(moisture_dirpath, exist_ok=True)
        
        df = pd.DataFrame( {
            '300hPa_湿数' : features['300hPa_lat35.60_long138.000_湿数'],
            '500hPa_湿数' : features['500hPa_lat35.60_long138.000_湿数'],
            '700hPa_湿数' : features['700hPa_lat35.60_long138.000_湿数'],
            '850hPa_湿数' : features['850hPa_lat35.60_long138.000_湿数'],
            '水戸_天気'     : lebel_data
        } )
        
        label = '水戸_天気'
        columns = [ '300hPa_湿数', '500hPa_湿数', '700hPa_湿数', '850hPa_湿数']
        
        ##################################################
        # 湿数 x 水戸-天気
        for column in columns:
            
            # KDEプロット
            grid = sns.FacetGrid(df, hue=label, aspect=2)
            grid.map(sns.kdeplot, column, shade=True)
            min_value, max_value = df[column].min(), df[column].max()
            grid.set(xlim=(min_value, max_value))
            grid.add_legend()
            filename = 'moisture_{0:s}_kdeplot.png'.format(column)
            kdeplot_file = os.path.join(moisture_dirpath, filename)
            grid.savefig(kdeplot_file)
            
            # ヒストグラム
            grid = sns.FacetGrid(df, col=label, height=3)
            grid.map(plt.hist, column, bins=20)
            grid.add_legend()
            filename = 'moisture_{0:s}_hist.png'.format(column)
            hist_file = os.path.join(moisture_dirpath, filename)
            grid.savefig(hist_file)
                
        ##################################################
        # 湿数同士の関係を可視化する
        pair_grid = sns.pairplot(df, hue=label);
        pair_file = os.path.join(moisture_dirpath, 'moisture_pairplot.png')
        pair_grid.savefig(pair_file)
        
        plt.close()
    
    ##################################################
    # 相当温位と水戸-天気の関係を可視化する
    ##################################################
    def _visualize_potential_temperature_and_weather(self, features, lebel_data, output_dirpath):
        
        ptemerature_dirpath = os.path.join(output_dirpath, 'potential_temperature')
        os.makedirs(ptemerature_dirpath, exist_ok=True)
        
        df = pd.DataFrame( {
            '300hPa_相当温位' : features['300hPa_lat33.20_long133.000_相当温位'] - 273.15,
            '500hPa_相当温位' : features['500hPa_lat33.20_long133.000_相当温位'] - 273.15,
            '700hPa_相当温位' : features['700hPa_lat33.20_long133.000_相当温位'] - 273.15,
            '850hPa_相当温位' : features['850hPa_lat33.20_long133.000_相当温位'] - 273.15,
            '水戸_天気'     : lebel_data
        } )
        
        label = '水戸_天気'
        columns = [ '300hPa_相当温位', '500hPa_相当温位', '700hPa_相当温位', '850hPa_相当温位']
        
        ##################################################
        # 相当温位 x 水戸-天気
        for column in columns:
            
            # KDEプロット
            grid = sns.FacetGrid(df, hue=label, aspect=2)
            grid.map(sns.kdeplot, column, shade=True)
            min_value, max_value = df[column].min(), df[column].max()
            grid.set(xlim=(min_value, max_value))
            grid.add_legend()
            filename = 'potential_temperature_{0:s}_kdeplot.png'.format(column)
            kdeplot_file = os.path.join(ptemerature_dirpath, filename)
            grid.savefig(kdeplot_file)
            
            # ヒストグラム
            grid = sns.FacetGrid(df, col=label, height=3)
            grid.map(plt.hist, column, bins=20)
            grid.add_legend()
            filename = 'potential_temperature_{0:s}_hist.png'.format(column)
            hist_file = os.path.join(ptemerature_dirpath, filename)
            grid.savefig(hist_file)
                
        ##################################################
        # 相当温位同士の関係を可視化する
        pair_grid = sns.pairplot(df, hue=label);
        pair_file = os.path.join(ptemerature_dirpath, 'potential_temperature_pairplot.png')
        pair_grid.savefig(pair_file)
        
        plt.close()
    
    ##################################################
    # 学習・評価・予測用のデータをロードする
    ##################################################
    def _load_data(self):
        
        # データ未読み込みの場合
        if self._is_data_loaded == False:
        
            # 気象データを読み込み
            loader = GsmLoader2020Ver3(
                self._base_dir, self._temp_dir, self._input_dir, self._label_name,
                self._input2_dir, self._gsm_thinout_interval, self._weather_convert_mode)
            df = loader.load()
            
            # 読み込んだデータをクラス変数に保存
            self._load_data = df
            
            # 読み込み済みフラグON
            self._is_data_loaded = True
            
        return self._load_data
        
    ##################################################
    # ロードしたデータから、ラベルデータを取得する
    ##################################################
    def _make_training_data(self, load_data):
        
        data_x = load_data.drop(columns=[self._label_name, ])
        data_y = load_data[self._label_name]
        
        # Xデータから末尾(最新時刻)のデータを削る
        features = data_x.iloc[:-2,]
        #features = data_x
        features = features.reset_index(drop=True)
        
        # Yデータから先頭(最旧時刻)のデータを削る
        label = data_y.iloc[2:,]
        #label = data_y
        label = label.reset_index(drop=True)
        
        # ラベルを数値から名称に変換する
        label = label.replace({0: '晴れ', 1: 'くもり', 2: '雨'})
        
        return features, label
        
    ##################################################
    # 解析用の列を追加する
    ##################################################
    def _add_columns_for_analysis(self, features):
        
        features['年'] = features['日付'].dt.year
        features['月'] = features['日付'].dt.month
        features['日'] = features['日付'].dt.day
        
        def concat_month_and_hour(row):
            month = row['月']
            hour = row['時']
            return '{0:02d}-{1:02d}'.format(month, hour)
            
        features['月-時'] = features.apply(concat_month_and_hour, axis=1)
        
        return features
