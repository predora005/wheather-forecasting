# coding: utf-8

from .abs_runner import AbsRunner
import os
#import wfile
import wdfproc
from loader import Loader
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
        
        # ディレクトリ名
        self.base_dir = os.getcwd()
        self.temp_dir = 'temp'
        self.input_dir = 'input2'
        self.output_dir = 'output'
        
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
        
            # 気象データを読み込み
            loader = Loader(self.base_dir, self.temp_dir, self.input_dir)
            df = loader.load()
            
            # NaNを置換する
            df = df.fillna(-9999)
    
            # 学習データ・テスト用データ作成
            self.train_x, self.train_y, self.test_x, self.test_y = \
                self.make_training_data(df, 'Mito_天気')
                
            self.is_data_loaded = True
            
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
        
        # 訓練データとテストデータに分割する
        #train_x, test_x, train_y, test_y = train_test_split(data_x, data_y, shuffle=True)
        train_x, test_x, train_y, test_y = train_test_split(data_x, data_y, shuffle=False, test_size=0.33)
        
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
        
        # 出力ディレクトリを作成する
        output_dir = os.path.join(self.base_dir, self.output_dir)
        os.makedirs(output_dir, exist_ok=True)
        
        fig_name = os.path.join(output_dir, 'feature_importances.png')
        plt.savefig(fig_name, bbox_inches='tight')
        
        csv_name = os.path.join(output_dir, 'feature_importances.csv')
        feature_importances.to_csv(csv_name)

    ##################################################
    # Graphvizのグラフをファイルに出力する
    ##################################################
    def export_graphviz(self):
        
        file_path = os.path.join(self.base_dir, self.output_dir, 'graphviz.png')
        estimators = self.model.get_estimators()[0] 
        feature_names = self.train_x.columns,
        class_names = self.class_names
    
        util.export_graphviz(file_path, estimators, feature_names, class_names)
        