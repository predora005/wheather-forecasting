# coding: utf-8

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

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
        
        # 積算降水量と水戸-天気の関係を可視化する
        self._visualize_total_precipitation_and_weather(features, label, output_dirpath)
        
        # 雲量と水戸-天気の関係を可視化する
        self._visualize_cloud_cover_and_weather(features, label, output_dirpath)
        
        # 気温と水戸-天気の関係を可視化する
        self._visualize_temperature_cover_and_weather(features, label, output_dirpath)
        
        # 気温と日付の関係を可視化する
        self._visualize_temperature_and_datetime(features, label, output_dirpath)
        
        # 高度と水戸-天気の関係を可視化する
        self._visualize_altitude_and_weather(features, label, output_dirpath)
        
        # 水戸-天気と日付の関係を可視化する
        self._visualize_weather_and_datetime(features, label, output_dirpath)
        
        # 風速と水戸-天気の関係を可視化する
        self._visualize_wind_and_weather(features, label, output_dirpath)
        
    ##################################################
    # 積算降水量と水戸-天気の関係を可視化する
    ##################################################
    def _visualize_total_precipitation_and_weather(self, features, lebel_data, output_dirpath):
        
        precipitation_dirpath = os.path.join(output_dirpath, 'total_precipitation')
        os.makedirs(precipitation_dirpath, exist_ok=True)
        
        #total_precipitation_24h = data['Surf_lat36.00_long140.000_積算降水量_24h']
        df = pd.DataFrame( {
            '月'            : features['月'],
            '積算降水量_03h': features['Surf_lat35.60_long140.000_積算降水量_03h'], 
            '積算降水量_06h': features['Surf_lat35.60_long140.000_積算降水量_06h'], 
            '積算降水量_12h': features['Surf_lat35.60_long140.000_積算降水量_12h'], 
            '積算降水量_24h': features['Surf_lat35.60_long140.000_積算降水量_24h'], 
            '水戸_天気': lebel_data
        } )
        
        label = '水戸_天気'
        data_set = [    ('積算降水量_03h', '03h'), ('積算降水量_06h', '06h'),
                        ('積算降水量_12h', '12h'), ('積算降水量_24h', '24h'), ]
        
        ##################################################
        # 積算降水量 x 水戸-天気
        for column, name in data_set:
            
            # KDEプロット
            grid = sns.FacetGrid(df, hue=label, aspect=2)
            grid.map(sns.kdeplot, column, shade=True)
            max_value = df[column].max()
            grid.set(xlim=(0, 20))
            grid.add_legend()
            filename = 'total_precipitation_{0:s}_kdeplot.png'.format(name)
            kdeplot_file = os.path.join(precipitation_dirpath, filename)
            grid.savefig(kdeplot_file)

            # ヒストグラム
            bins = np.arange(0, 30, 1)
            grid = sns.FacetGrid(df, col=label, height=3)
            grid.map(plt.hist, column, bins=bins)
            grid.add_legend()
            filename = 'total_precipitation_{0:s}_hist.png'.format(name)
            hist_file = os.path.join(precipitation_dirpath, filename)
            grid.savefig(hist_file)

        ##################################################
        # 月ごとの風速と天気の関係を可視化する
        for column, name in data_set:
            
            plot = sns.relplot(x='月', y=column, hue=label, kind='line', ci="sd", data=df)
            filename = 'total_precipitation_{0:s}_month_lineplot.png'.format(name)
            lineplot_file = os.path.join(precipitation_dirpath, filename)
            plot.savefig(lineplot_file)
        
        ##################################################
        # 積算降水量同士の関係を可視化する
        df = df.drop(columns=['月'])
        pair_grid = sns.pairplot(df, hue=label);
        pair_file = os.path.join(precipitation_dirpath, 'total_precipitation_pairplot.png')
        pair_grid.savefig(pair_file)
        
        plt.close()
        
    ##################################################
    # 雲量と水戸-天気の関係を可視化する
    ##################################################
    def _visualize_cloud_cover_and_weather(self, features, lebel_data, output_dirpath):
        
        cloud_dirpath = os.path.join(output_dirpath, 'cloud')
        os.makedirs(cloud_dirpath, exist_ok=True)
        
        #total_precipitation_24h = data['Surf_lat36.00_long138.000_上層雲量']
        df = pd.DataFrame( {
            '上層雲量': features['Surf_lat36.40_long135.000_上層雲量'],
            '中層雲量': features['Surf_lat36.40_long135.000_中層雲量'],
            '下層雲量': features['Surf_lat36.40_long135.000_下層雲量'],
            '全雲量'  : features['Surf_lat36.40_long135.000_全雲量'],
            '水戸_天気': lebel_data
        } )
        
        label = '水戸_天気'
        columns = [ '上層雲量', '中層雲量', '下層雲量', '全雲量',]
        
        ##################################################
        # 雲量 x 水戸-天気
        for column in columns:
            
            # KDEプロット
            grid = sns.FacetGrid(df, hue=label, aspect=2)
            grid.map(sns.kdeplot, column, shade=True)
            max_value = df[column].max()
            grid.set(xlim=(0, max_value))
            grid.add_legend()
            filename = 'cloud_cover_{0:s}_kdeplot.png'.format(column)
            kdeplot_file = os.path.join(cloud_dirpath, filename)
            grid.savefig(kdeplot_file)
            
            # ヒストグラム
            bins = np.arange(0, 100, 5)
            grid = sns.FacetGrid(df, col=label, height=3)
            grid.map(plt.hist, column, bins=bins)
            grid.add_legend()
            filename = 'cloud_cover_{0:s}_hist.png'.format(column)
            hist_file = os.path.join(cloud_dirpath, filename)
            grid.savefig(hist_file)
                
        ##################################################
        # 雲量同士の関係を可視化する
        pair_grid = sns.pairplot(df, hue=label);
        pair_file = os.path.join(cloud_dirpath, 'cloud_cover_pairplot.png')
        pair_grid.savefig(pair_file)
        
        plt.close()
        
    ##################################################
    # 気温と水戸-天気の関係を可視化する
    ##################################################
    def _visualize_temperature_cover_and_weather(self, features, lebel_data, output_dirpath):
        
        temp_dirpath = os.path.join(output_dirpath, 'temperature')
        os.makedirs(temp_dirpath, exist_ok=True)
        
        df = pd.DataFrame( {
            '500hPa_気温': features['500hPa_lat37.20_long138.000_気温'],
            '700hPa_気温': features['700hPa_lat37.20_long138.000_気温'],
            '850hPa_気温': features['850hPa_lat37.20_long138.000_気温'],
            '地上_気温'  : features['Surf_lat37.20_long138.000_気温'],
            '水戸_天気': lebel_data
        } )
        
        label = '水戸_天気'
        columns = [ '500hPa_気温', '700hPa_気温', '850hPa_気温', '地上_気温',]
        
        # ケルビンから摂氏に変換する
        for column in columns:
            df[column] = df[column] - 273.15
        
        # 気温 x 水戸-天気
        for column in columns:
            
            # KDEプロット
            grid = sns.FacetGrid(df, hue=label, aspect=2)
            grid.map(sns.kdeplot, column, shade=True)
            min_value, max_value = df[column].min(), df[column].max()
            grid.set(xlim=(min_value, max_value))
            grid.add_legend()
            filename = 'temperature_{0:s}_kdeplot.png'.format(column)
            kdeplot_file = os.path.join(temp_dirpath, filename)
            grid.savefig(kdeplot_file)
            
            # ヒストグラム
            #bins = np.arange(0, max_value, 1)
            grid = sns.FacetGrid(df, col=label, height=3)
            grid.map(plt.hist, column, bins=20)
            grid.add_legend()
            filename = 'temperature_{0:s}_hist.png'.format(column)
            hist_file = os.path.join(temp_dirpath, filename)
            grid.savefig(hist_file)
                
        ##################################################
        # 気温同士の関係を可視化する
        pair_grid = sns.pairplot(df, hue=label);
        pair_file = os.path.join(temp_dirpath, 'temperature_pairplot.png')
        pair_grid.savefig(pair_file)
        
        plt.close()

    ##################################################
    # 気温と水戸-天気の関係を可視化する
    ##################################################
    def _visualize_temperature_and_datetime(self, features, lebel_data, output_dirpath):
        
        temp_dirpath = os.path.join(output_dirpath, 'temperature')
        os.makedirs(temp_dirpath, exist_ok=True)
        
        df = pd.DataFrame( {
            '月'            : features['月'],
            '月-時'         : features['月-時'],
            '500hPa_気温'   : features['500hPa_lat37.20_long138.000_気温'] - 273.15,
            '700hPa_気温'   : features['700hPa_lat37.20_long138.000_気温']- 273.15,
            '850hPa_気温'   : features['850hPa_lat37.20_long138.000_気温']- 273.15,
            '地上_気温'     : features['Surf_lat37.20_long138.000_気温']- 273.15,
            '水戸_天気'     : lebel_data
        })
        
        label = '水戸_天気'
        columns = [ '500hPa_気温', '700hPa_気温', '850hPa_気温', '地上_気温',]
        
        ##################################################
        # 月ごとの気温と天気の関係を可視化する
        for column in columns:
            
            plot = sns.relplot(x='月', y=column, hue=label, kind='line', ci="sd", data=df)
            filename = 'temperature_{0:s}_month_lineplot.png'.format(column)
            lineplot_file = os.path.join(temp_dirpath, filename)
            plot.savefig(lineplot_file)
        
            plot = sns.catplot(x='月', y=column, hue=label, kind='swarm', data=df)
            filename = 'temperature_{0:s}_month_catplot.png'.format(column)
            catplot_file = os.path.join(temp_dirpath, filename)
            plot.savefig(catplot_file)
        
        ##################################################
        # 月-時ごとの気温と天気の関係を可視化する
        for column in columns:
            
            plot = sns.relplot(x='月-時', y=column, hue=label, kind='line', ci="sd", data=df, aspect=4)
            filename = 'temperature_{0:s}_month_hour_lineplot.png'.format(column)
            lineplot_file = os.path.join(temp_dirpath, filename)
            plot.savefig(lineplot_file)
        
        #month_hour_mean = df.groupby('月').mean()
        
        plt.close()
        
    ##################################################
    # 高度と水戸-天気の関係を可視化する
    ##################################################
    def _visualize_altitude_and_weather(self, features, lebel_data, output_dirpath):
        
        altitude_dirpath = os.path.join(output_dirpath, 'altitude')
        os.makedirs(altitude_dirpath, exist_ok=True)
        
        df = pd.DataFrame( {
            '月'            : features['月'],
            '月-時'         : features['月-時'],
            '500hPa_高度'   : features['500hPa_lat34.80_long136.000_高度'],
            '700hPa_高度'   : features['700hPa_lat34.80_long136.000_高度'],
            '850hPa_高度'   : features['850hPa_lat34.80_long136.000_高度'],
            '地上_海面気圧' : features['Surf_lat34.80_long136.000_海面更正気圧'] / 100,
            '水戸_天気'     : lebel_data
        } )
        
        label = '水戸_天気'
        columns = [ '500hPa_高度', '700hPa_高度', '850hPa_高度', '地上_海面気圧']
        
        ##################################################
        # 高度 x 水戸-天気
        for column in columns:
            
            # KDEプロット
            grid = sns.FacetGrid(df, hue=label, aspect=2)
            grid.map(sns.kdeplot, column, shade=True)
            min_value, max_value = df[column].min(), df[column].max()
            grid.set(xlim=(min_value, max_value))
            grid.add_legend()
            filename = 'altitude_{0:s}_kdeplot.png'.format(column)
            kdeplot_file = os.path.join(altitude_dirpath, filename)
            grid.savefig(kdeplot_file)
            
            # ヒストグラム
            #bins = np.arange(0, max_value, 1)
            grid = sns.FacetGrid(df, col=label, height=3)
            grid.map(plt.hist, column, bins=20)
            grid.add_legend()
            filename = 'altitude_{0:s}_hist.png'.format(column)
            hist_file = os.path.join(altitude_dirpath, filename)
            grid.savefig(hist_file)
                
        ##################################################
        # 月ごとの高度と天気の関係を可視化する
        for column in columns:
            
            plot = sns.relplot(x='月', y=column, hue=label, kind='line', ci="sd", data=df)
            filename = 'altitude_{0:s}_month_lineplot.png'.format(column)
            lineplot_file = os.path.join(altitude_dirpath, filename)
            plot.savefig(lineplot_file)
        
        ##################################################
        # 高度同士の関係を可視化する
        altitude_df = df.drop(columns=['月', '月-時'])
        pair_grid = sns.pairplot(altitude_df, hue=label);
        pair_file = os.path.join(altitude_dirpath, 'altitude_pairplot.png')
        pair_grid.savefig(pair_file)
        
        plt.close()
    
    ##################################################
    # 水戸-天気と日付の関係を可視化する
    ##################################################
    def _visualize_weather_and_datetime(self, features, lebel_data, output_dirpath):
        
        weather_dirpath = os.path.join(output_dirpath, 'weather')
        os.makedirs(weather_dirpath, exist_ok=True)
        
        df = pd.DataFrame( {
            '月'            : features['月'],
            '月-時'         : features['月-時'],
            '水戸_天気'     : lebel_data
        })
        
        label = '水戸_天気'

        ##################################################
        # 月ごとの天気を可視化する
        plot = sns.catplot(x='月', hue=label, kind='count', data=df)
        catplot_file = os.path.join(weather_dirpath, 'weather_month_catplot.png')
        plot.savefig(catplot_file)
        
        ##################################################
        # 月-時ごとの天気を可視化する
        plot = sns.catplot(x='月-時', hue=label, kind='count', data=df, aspect=4)
        catplot_file = os.path.join(weather_dirpath, 'weather_month_hour_catplot.png')
        plot.savefig(catplot_file)
        
        plt.close()
    
    ##################################################
    # 風速と水戸-天気の関係を可視化する
    ##################################################
    def _visualize_wind_and_weather(self, features, lebel_data, output_dirpath):
        
        wind_dirpath = os.path.join(output_dirpath, 'wind_u')
        os.makedirs(wind_dirpath, exist_ok=True)
        
        df = pd.DataFrame( {
            '月'            : features['月'],
            '月-時'         : features['月-時'],
            '500hPa_東西風' : features['500hPa_lat35.60_long140.000_東西風'],
            '700hPa_東西風' : features['700hPa_lat35.60_long140.000_東西風'],
            '850hPa_東西風' : features['850hPa_lat35.60_long140.000_東西風'],
            '地上_東西風'   : features['Surf_lat35.60_long140.000_東西風'],
            '水戸_天気'     : lebel_data
        } )
        
        label = '水戸_天気'
        columns = [ '500hPa_東西風', '700hPa_東西風', '850hPa_東西風', '地上_東西風']
        
        ##################################################
        # 東西風 x 水戸-天気
        for column in columns:
            
            # KDEプロット
            grid = sns.FacetGrid(df, hue=label, aspect=2)
            grid.map(sns.kdeplot, column, shade=True)
            min_value, max_value = df[column].min(), df[column].max()
            grid.set(xlim=(min_value, max_value))
            grid.add_legend()
            filename = 'wind_u_{0:s}_kdeplot.png'.format(column)
            kdeplot_file = os.path.join(wind_dirpath, filename)
            grid.savefig(kdeplot_file)
            
            # ヒストグラム
            #bins = np.arange(0, max_value, 1)
            grid = sns.FacetGrid(df, col=label, height=3)
            grid.map(plt.hist, column, bins=20)
            grid.add_legend()
            filename = 'wind_u_{0:s}_hist.png'.format(column)
            hist_file = os.path.join(wind_dirpath, filename)
            grid.savefig(hist_file)
                
        ##################################################
        # 月ごとの風速と天気の関係を可視化する
        for column in columns:
            
            plot = sns.relplot(x='月', y=column, hue=label, kind='line', ci="sd", data=df)
            filename = 'wind_u_{0:s}_month_lineplot.png'.format(column)
            lineplot_file = os.path.join(wind_dirpath, filename)
            plot.savefig(lineplot_file)
        
        ###################################################
        # 風速同士の関係を可視化する
        wind_df = df.drop(columns=['月', '月-時'])
        pair_grid = sns.pairplot(wind_df, hue=label);
        pair_file = os.path.join(wind_dirpath, 'wind_u_pairplot.png')
        pair_grid.savefig(pair_file)
        
        plt.close()
        
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
