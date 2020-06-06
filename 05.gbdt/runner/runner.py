# coding: utf-8

from .abs_runner import AbsRunner
import os
import wfile
import wdfproc
import util
import pandas as pd

from sklearn.model_selection import train_test_split, KFold, StratifiedKFold

import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.font_manager._rebuild() #キャッシュの削除
plt.rcParams['font.family'] = 'IPAGothic' # インストールしたフォントを指定

##################################################
# 学習・評価・予測 実行クラス
##################################################
class Runner(AbsRunner):
    """学習・評価・予測 実行クラス
        
    Attributes:
        属性の名前 (属性の型): 属性の説明
        属性の名前 (:obj:`属性の型`): 属性の説明.
    """
    
    ##################################################
    # コンストラクタ
    ##################################################
    def __init__(self, run_name, model, params):
        
        # 抽象クラスのコンストラクタ
        super(Runner, self).__init__(run_name, model, params)
        
        # データ読み込み済みフラグ
        self.is_data_loaded = False
        
        # 学習・予測用データ
        self.train_x = None
        self.train_y = None
        self.test_x = None
        self.test_y = None
        
        # クラス名
        self.class_names=['Sunny', 'Cloud', 'Rain', 'Other']
        
    ##################################################
    # foldを指定して学習・評価を行う
    ##################################################
    def run_train_fold(self, fold):
        raise NotImplementedError()

    ##################################################
    # クロスバリデーションで学習・評価を行う
    ##################################################
    def run_train_cv(self):
        
        # データをロードする
        self.load_data()
        
        #fold = StratifiedKFold(n_splits=3)
        fold = KFold(n_splits=3)
        for i, (train_index, test_index) in enumerate(fold.split(self.train_x, self.train_y)):
            
            # 訓練データを抽出する
            tx = self.train_x.iloc[train_index]
            ty = self.train_y.iloc[train_index]
            
            # 検証データを抽出する
            vx = self.train_x.iloc[test_index]
            vy = self.train_y.iloc[test_index]
            
            # 学習を行う
            self.model.train(tx, ty)
            
            # 予測を行う
            pred_y = self.model.predict(vx) 
            
            # 評価結果を出力する
            run_fold_name = '{0:s}_fold_{1:02d}'.format(self.run_name, i) 
            print('#################################')
            print('  {0:s}'.format(run_fold_name))
            print('#################################')
            util.print_accuracy(vy, pred_y, self.class_names)
            
    def run_predict_cv(self):
        raise NotImplementedError()
        
    def run_train_all(self):
        self.load_data()
        self.model.train(self.train_x, self.train_y)
    
    ##################################################
    # 学習データ全てを学習したモデルで、テストデータの予測を行う
    ##################################################
    def run_predict_all(self):
        
        # データをロードする
        self.load_data()
        
        pred_y = self.model.predict(self.test_x)
        self.pred_y = pred_y
        
        print('#################################')
        print('  {0:s}'.format(self.run_name))
        print('#################################')
        util.print_accuracy(self.test_y, pred_y, self.class_names)
        
    ##################################################
    # 学習・評価・予測用のデータをロードする
    ##################################################
    def load_data(self):
        
        # データ未読み込みの場合
        if not (self.is_data_loaded):
        
            # 地上気象データを取得する
            gdf = self.get_ground_weather()
            
            # 高層気象データを取得する
            hdf = self.get_highrise_weather()
            
            # 地上気象データと高層気象データをマージする
            df = pd.merge(gdf, hdf, on=('日付','時'))
            
            # NaNを置換する
            df = df.fillna(-9999)
    
            # 学習データ・テスト用データ作成
            self.train_x, self.train_y, self.test_x, self.test_y = \
                self.make_training_data(df, 'Mito_天気')
                
            self.is_data_loaded = True

    ##################################################
    # 地上気象データ取得
    ##################################################
    def get_ground_weather(self):
        
        # カレントディレクトリを取得する
        cwd = os.getcwd()
        
        # tempディレクトリを作成する
        os.makedirs('temp', exist_ok=True)
    
        # 地上気象データを取得する
        ground_weather_csv = 'temp/ground_weather.csv'
        if os.path.isfile(ground_weather_csv):
            ground_df = pd.read_csv(ground_weather_csv, index_col=0, parse_dates=[1])
            
        else:
            ground_dir = os.path.join(cwd, 'ground_weather')
            ground_df = wfile.get_ground_weather(ground_dir)
            ground_df.to_csv(ground_weather_csv)
            
        # 天気記号を数値に変換する
        ground_df = wdfproc.convert_symbol_to_number(ground_df)
        
        # 地上気象データからNaNが含まれる列を削る
        ground_df = wdfproc.drop_unneeded_ground(ground_df)
        ground_df.to_csv('ground2.csv')
        
        # 風速・風向きを数値に変換する
        ground_df = wdfproc.convert_wind_to_vector_ground(ground_df)
        ground_df.to_csv('ground3.csv')
        
        # 天気を数値に変換する
        ground_df = wdfproc.convert_weather_to_interger(ground_df)
        ground_df.to_csv('ground4.csv')
        
        # 雲量を浮動小数点数に変換する
        ground_df = wdfproc.convert_cloud_volume_to_float(ground_df)
        ground_df.to_csv('ground5.csv')
        
        # 天気を指定した境界値で分類する
        #  - 水戸は3分割、それ以外は○分割にする
        weather_cols = [col for col in ground_df.columns if('天気' in col)]
        weather_cols.pop( weather_cols.index('Mito_天気') )
        ground_df = wdfproc.replace_weather(
                            ground_df, columns=weather_cols, 
                             mode=wdfproc.WeatherConvertMode.Coarse)
        ground_df.to_csv('ground6.csv')
        ground_df = wdfproc.replace_weather(ground_df, columns=['Mito_天気'])
        ground_df.to_csv('ground7.csv')
        
        # 浮動小数点数を32ビットに変換する
        ground_df = wdfproc.type_to_float32(ground_df)
        ground_df.to_csv('ground8.csv')
        
        # 不要な列を除去する
        ground_df = wdfproc.drop_columns(
            ground_df, 
            #[ '現地気圧', '海面気圧', '気温', '露点温度', '蒸気圧', '日照時間', 
            #  '降雪', '積雪', '雲量', '視程', '全天日射', '降水量', '風速' ]
            [ '現地気圧', '海面気圧', '気温', '露点温度', '蒸気圧', '日照時間', 
              '降雪', '積雪', '雲量', '視程', '全天日射', '降水量' ]
        )
        ground_df.to_csv('ground9.csv')
    
        print(ground_df.info())
    
        return ground_df
        
    
    ##################################################
    # 高層気象データ取得
    ##################################################
    def get_highrise_weather(self):
        
        # カレントディレクトリを取得する
        cwd = os.getcwd()
        
        # tempディレクトリを作成する
        os.makedirs('temp', exist_ok=True)
        
        # 高層気象データを取得する
        highrise_weather_csv = 'temp/highrise_weather.csv'
        if os.path.isfile(highrise_weather_csv):
            highrise_df = pd.read_csv(highrise_weather_csv, index_col=0, parse_dates=[1])
        else:
            highrise_dir = os.path.join(cwd, 'highrise_weather')
            highrise_df = wfile.get_highrise_weather(highrise_dir)
            highrise_df.to_csv(highrise_weather_csv)
        
        # 高層気象データから不要データを除去する
        #highrise_df = wdfproc.drop_unneeded_higirise(highrise_df)
        #highrise_df.to_csv('highrise2.csv')
        
        # 風速・風向きを数値に変換する
        highrise_df = wdfproc.convert_wind_to_vector_highrise(highrise_df)
        highrise_df.to_csv('highrise2.csv')
        
        # 浮動小数点数を32ビットに変換する
        highrise_df = wdfproc.type_to_float32(highrise_df)
        highrise_df.to_csv('highrise3.csv')
        
        # 不要な列を除去する
        highrise_df = wdfproc.drop_columns(
            highrise_df, 
            [ '高度', '1000', '925', '900', '800', '600', '400']
        )
        highrise_df.to_csv('highrise4.csv')
    
        print(highrise_df.info())
        
        return highrise_df
        
    ##################################################
    # 学習データ作成
    ##################################################
    def make_training_data(self, df, y_name):
        
        df = df.drop(columns=['時', '日付'])
        
        data_x = df.drop(columns=[y_name, ])
        data_y = df[y_name]
    
        # Xデータから末尾(最新時刻)のデータを削る
        data_x = data_x.iloc[:-1,]
    
        # Yデータから先頭(最旧時刻)のデータを削る
        data_y = data_y.iloc[1:,]
    
        train_x, test_x, train_y, test_y = train_test_split(data_x, data_y, shuffle=True)
    
        return train_x, train_y, test_x, test_y
    
    ##################################################
    # 特徴量の重要度を表示する
    ##################################################
    def show_importance_of_feature(self):
        
        train_x = self.train_x
        
        importances = self.model.get_feature_importances()
        columns = train_x.columns
        feature_importances = pd.DataFrame(importances, index=train_x.columns, columns=['Importance'])
        feature_importances = feature_importances.sort_values(by='Importance', ascending=False)
        feature_importances.plot(kind='bar', figsize=(20,20))
        plt.savefig('feature_importances.png', bbox_inches='tight')
        
        # tempディレクトリを作成する
        os.makedirs('result', exist_ok=True)
        
        feature_importances.to_csv('result/feature_importances.csv')


