# coding: utf-8

from .abs_runner import AbsRunner
import os
import wdfproc
from loader import GsmLoader
import util
import pandas as pd

from sklearn.model_selection import train_test_split, KFold, StratifiedKFold

##################################################
# GSMデータを用いた学習・評価・予測 実行クラス
##################################################
class GsmForecastRunner(AbsRunner):
    """ GSMデータを用いた学習・評価・予測 実行クラス

    Attributes:
        run_name (string)   : ランの名称
        model (AbsModel)    : モデル
        params (dict)       : パラメータ
    """
    
    ##################################################
    # コンストラクタ
    ##################################################
    def __init__(self, run_name, model, params):
        
        # 抽象クラスのコンストラクタ
        super().__init__(run_name, model, params)
        
        # 各種フラグ
        self._is_data_loaded = False # データ読み込み済みフラグ
        self._is_trained_all = False # 全データで学習済みフラグ
        
        # 学習・予測用データ
        self._train_x = None
        self._train_y = None
        self._test_x = None
        self._test_y = None
        
        # ディレクトリ名
        self._base_dir = os.getcwd()
        self._temp_dir = 'temp'
        self._input_dir = 'input4'
        self._input2_dir = 'input2'
        self._output_dir = 'output'
        
        # クラス名
        self._class_names=['Sunny', 'Cloud', 'Rain', 'Other']
        
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
        self._load_data()
        
        #fold = StratifiedKFold(n_splits=3)
        fold = KFold(n_splits=3)
        for i, (train_index, test_index) in enumerate(fold.split(self._train_x, self._train_y)):
            
            # 訓練データを抽出する
            tx = self._train_x.iloc[train_index]
            ty = self._train_y.iloc[train_index]
            
            # 検証データを抽出する
            vx = self._train_x.iloc[test_index]
            vy = self._train_y.iloc[test_index]
            
            # 学習を行う
            self._model.train(tx, ty)
            
            # 予測を行う
            pred_y = self._model.predict(vx) 
            
            # 評価結果を出力する
            run_fold_name = '{0:s}_fold_{1:02d}'.format(self._run_name, i) 
            print('#################################')
            print('  {0:s}'.format(run_fold_name))
            print('#################################')
            util.print_accuracy(vy, pred_y, self._class_names)
            
    ##################################################
    # クロスバリデーションで学習した
    # 各foldモデルの平均で予測を行う
    ##################################################
    def run_predict_cv(self):
        raise NotImplementedError()
        
    ##################################################
    # 学習データ全てを使用して、学習を行う
    ##################################################
    def run_train_all(self):
        self._load_data()
        self._model.train(self._train_x, self._train_y)
        self.is_trained_all = True
    
    ##################################################
    # 学習データ全てを学習したモデルで、テストデータの予測を行う
    ##################################################
    def run_predict_all(self):
        
        # 全データで学習済みか
        if self.is_trained_all:
        
            # 予測を行う
            pred_y = self._model.predict(self._test_x)
            self._pred_y = pred_y
            
            # 正解率を表示する
            print('#################################')
            print('  {0:s}'.format(self._run_name))
            print('#################################')
            util.print_accuracy(self._test_y, pred_y, self._class_names)
            
            # 特徴量の重要度を表示する
            self._show_importance_of_feature()

            # Graphvizのグラフをファイルに出力する
            self._export_graphviz()

    ##################################################
    # 学習・評価・予測用のデータをロードする
    ##################################################
    def _load_data(self):
        
        # データ未読み込みの場合
        if not (self._is_data_loaded):
        
            # 気象データを読み込み
            loader = GsmLoader(self._base_dir, self._temp_dir, self._input_dir, self._input2_dir)
            df = loader.load()
            
            # NaNを置換する
            df = df.fillna(-9999)
    
            # 学習データ・テスト用データ作成
            self._train_x, self._train_y, self._test_x, self._test_y = \
                self._make_training_data(df, 'Mito_天気')
                
            self.is_data_loaded = True
            
    ##################################################
    # 学習データ作成
    ##################################################
    def _make_training_data(self, df, label_name):
        
        df = df.drop(columns=['時', '日付'])
        
        data_x = df.drop(columns=[label_name, ])
        data_y = df[label_name]
        
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
    def _show_importance_of_feature(self):
        
        # 重要度と特徴量の名称を取得する
        importances = self._model.get_feature_importances()
        feature_names = self._train_x.columns
        
        # 出力ディレクトリを作成する
        output_dir = os.path.join(self._base_dir, self._output_dir)
        os.makedirs(output_dir, exist_ok=True)
        
        # 出力先のファイルパスを設定する
        fig_path = os.path.join(output_dir, 'feature_importances.png')
        csv_path = os.path.join(output_dir, 'feature_importances.csv')

        util.show_importance_of_feature(importances, feature_names, fig_path, csv_path)

    ##################################################
    # Graphvizのグラフをファイルに出力する
    ##################################################
    def _export_graphviz(self):
        
        file_path = os.path.join(self._base_dir, self._output_dir, 'graphviz.png')
        estimators = self._model.get_estimators()[0] 
        feature_names = self._train_x.columns
        class_names = self._class_names
    
        util.export_graphviz(file_path, estimators, feature_names, class_names)
        