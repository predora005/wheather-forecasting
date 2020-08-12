# coding: utf-8

from .abs_runner import AbsRunner

import os
import copy
import pandas as pd
import keras

import util
from loader import GsmLoader2020Ver3
from model import ModelXgboost, ModelDnn

from sklearn.model_selection import train_test_split, KFold, StratifiedKFold

##################################################
# GSMデータを用いた学習・評価・予測 実行クラス
# 2020 Ver3。
# 改善版。
##################################################
class GsmForecastRunner2020Ver3(AbsRunner):
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
        
    ##################################################
    # foldを指定して学習・評価を行う
    ##################################################
    def run_train_fold(self, fold):
        raise NotImplementedError()

    ##################################################
    # クロスバリデーションで学習・評価を行う
    ##################################################
    def run_train_cv(self, fold_splits):
        
        # データをロードする
        self._load_data()
        
        # モデルをクロスバリデーションの分割数分作成する
        self._cv_models = []
        for i in range(fold_splits):
            model = copy.deepcopy(self._model)
            self._cv_models.append(model)
        
        fold = KFold(n_splits=fold_splits, shuffle=False)
        for i, (train_index, test_index) in enumerate(fold.split(self._whole_x, self._whole_y)):
            
            model = self._cv_models[i]
            
            # 訓練データを抽出する
            tx = self._whole_x.iloc[train_index]
            ty = self._whole_y.iloc[train_index]
            
            # 検証データを抽出する
            vx = self._whole_x.iloc[test_index]
            vy = self._whole_y.iloc[test_index]
            
            # モデルがDNNの場合はデータを正規化する
            if type(self._model) is ModelDnn:
                # Max-Minスケール化
                #scaler, tx, vx = util.max_min_scale(tx, vx)
                # 標準化
                scaler, tx, vx = util.standardize(tx, vx)
                
            # 学習を行う
            run_fold_name = '{0:s}_fold_{1:02d}'.format(self._run_name, i) 
            model.train(tx, ty, vx, vy)
            
            # 予測を行う
            pred_y = model.predict(vx) 
            
            # 評価結果を出力する
            self._print_evaluation_score(model, run_fold_name, vy, pred_y)
            
            # 特徴量の重要度を表示する
            self._show_importance_of_feature(model, run_fold_name)
            
            # Graphvizのグラフをファイルに出力する
            self._export_graphviz(model, run_fold_name)
            
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
        
        # データをロードする
        self._load_data()
        train_x, train_y = self._train_x, self._train_y
        
        # モデルがDNNの場合はデータを正規化する
        if type(self._model) is ModelDnn:
            # Max-Minスケール化
            #self._train_all_scaler, train_x, _ = util.max_min_scale(train_x, None)
            # 標準化
            self._train_all_scaler, train_x, _ = util.standardize(train_x, None)
            
        self._model.train(train_x, train_y)
        self.is_trained_all = True
    
        # 学習モデルを保存する
        self._model.save_model()
            
    ##################################################
    # 学習データ全てを学習したモデルで、テストデータの予測を行う
    ##################################################
    def run_predict_all(self):
        
        # 全データで学習済みか
        if self.is_trained_all:
            
            test_x = self._test_x
            
            # モデルがDNNの場合は学習時に使用したスケーラで正規化する
            if type(self._model) is ModelDnn:
                test_x = self._train_all_scaler.transform(test_x)
            
            # 予測を行う
            pred_y = self._model.predict(test_x)
            self._pred_y = pred_y
            
            # 評価結果を出力する
            self._print_evaluation_score(self._model, self._run_name, test_y, pred_y)
            
            # 特徴量の重要度を表示する
            print('  show_importance_of_feature...')
            self._show_importance_of_feature(self._model, self._run_name)
            
            # Graphvizのグラフをファイルに出力する
            print('  export_graphviz...')
            self._export_graphviz(self._model, self._run_name)
            
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
            
            # 浮動小数点を32ビットに変更する
            df = util.type_to_float32(df)
            
            # NaNを置換する
            if type(self._model) is ModelDnn:
                # DNNの場合は平均値で置換する
                df = util.fill_na_avg(df)
            elif type(self._model) is ModelXgboost:
                # XGBoostの場合はNaNのままで問題無し
                pass
            
            # 学習データ・テスト用データ作成
            self._whole_x, self._whole_y, self._train_x, self._train_y, self._test_x, self._test_y = \
                self._make_training_data(df, self._label_name)
                
            # ラベル数をモデルに渡す
            self._label_num = self._train_y.nunique()
            self._model.add_param('label_num', self._label_num)
                
            self._is_data_loaded = True
            
    ##################################################
    # 学習データ作成
    ##################################################
    def _make_training_data(self, df, label_name):
        
        df = df.drop(columns=['時', '日付'])
        
        data_x = df.drop(columns=[label_name, ])
        data_y = df[label_name]
        
        # Xデータから末尾(最新時刻)のデータを削る
        whole_x = data_x.iloc[:-2,]
        
        # Yデータから先頭(最旧時刻)のデータを削る
        whole_y = data_y.iloc[2:,]
        
        # 訓練データとテストデータに分割する
        #train_x, test_x, train_y, test_y = train_test_split(data_x, data_y, shuffle=True)
        #train_x, test_x, train_y, test_y = train_test_split(data_x, data_y, shuffle=False, test_size=0.25)
        train_x, test_x, train_y, test_y = self._train_test_split(whole_x, whole_y, 4, [3])
        
        return whole_x, whole_y, train_x, train_y, test_x, test_y
    
    ##################################################
    # 学習データ作成
    ##################################################
    def _train_test_split(self, data_x, data_y, split_num, test_no):
        
        train_x = None
        test_x = None
        train_y = None
        test_y = None
        
        # 指定した分割数で分割する
        one_block_num = float(len(data_x) / split_num)
        for no in range(split_num):
            
            start_i = round( float(no) * one_block_num)
            end_i = round( float(no + 1) * one_block_num)
            
            # 分割
            split_x = data_x.iloc[start_i:end_i,]
            split_y = data_y.iloc[start_i:end_i,]
            
            if no in test_no:
                # テスト用データ
                if test_x is None:
                    test_x, test_y = split_x, split_y
                else:
                    test_x = test_x.append(split_x)
                    test_y = test_y.append(split_y)
            else:
                # 学習用データ
                if train_x is None:
                    train_x, train_y = split_x, split_y
                else:
                    train_x = train_x.append(split_x)
                    train_y = train_y.append(split_y)
        
        return train_x, test_x, train_y, test_y
    
    ##################################################
    # 評価結果を出力する
    ##################################################
    def _print_evaluation_score(self, model, run_fold_name, test_y, pred_y):
        
        print('#################################')
        print('  {0:s}'.format(run_fold_name))
        print('#################################')
        if type(model) is ModelDnn:
            # モデルがDNNの場合はOne-Hotラベル表現用の正解率を表示する
            test_y_onehot = keras.utils.to_categorical(test_y, num_classes=self._label_num)
            util.print_accuracy_one_hot(test_y_onehot, pred_y, self._class_names)
            util.print_precision_and_recall_one_hot(test_y_onehot, pred_y, self._class_names)
        else:
            util.print_accuracy(test_y, pred_y, self._class_names)
            util.print_precision_and_recall(test_y, pred_y, self._class_names)
            
    ##################################################
    # 特徴量の重要度を表示する
    ##################################################
    def _show_importance_of_feature(self, model, run_fold_name):
        
        # XGBoostの場合
        if type(model) is ModelXgboost:
            
            # 出力ディレクトリを作成する
            output_dir = os.path.join(self._base_dir, self._output_dir, self._run_name)
            os.makedirs(output_dir, exist_ok=True)
            
            # 特徴量の重要度をプロットする
            fig_file = 'freature_importances_{0:s}.png'.format(run_fold_name)
            fig_path = os.path.join(output_dir, fig_file)
            model.plot_feature_importances(fig_path)
            
            # 特徴量の重要度(ゲイン)を出力する
            gain_file = 'freature_importances_{0:s}_gain.csv'.format(run_fold_name)
            gain_path = os.path.join(output_dir, gain_file)
            gain = model.get_gain()
            util.output_importance_of_feature_for_xgboost(gain, gain_path)
            
            # 特徴量の重要度(Weight: 頻度)を出力する
            weight_file = 'freature_importances_{0:s}_weight.csv'.format(run_fold_name)
            weight_path = os.path.join(output_dir, weight_file)
            weight = model.get_weight()
            util.output_importance_of_feature_for_xgboost(weight, weight_path)

    ##################################################
    # Graphvizのグラフをファイルに出力する
    ##################################################
    def _export_graphviz(self, model, run_fold_name):
        
        # XGBoostの場合
        if type(model) is ModelXgboost:
            
            #file_name = 'decision_tree_{0:s}.png'.format(run_fold_name)
            #file_path = os.path.join(self._base_dir, self._output_dir, self._run_name, file_name)
            
            dir_path = os.path.join(self._base_dir, self._output_dir, self._run_name, 'dtree')
            file_prefix = 'decision_tree_{0:s}'.format(run_fold_name)
            num_trees = 3
            
            model.export_graphviz(dir_path, file_prefix, num_trees)
            