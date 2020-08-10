# coding: utf-8
"""
    2019年の天気予測モデル。
    入力は、9地点(水戸,前橋,東京,静岡,大阪,秩父,河口湖,新潟,宇都宮)の気象データ。
    出力は、水戸の3時間後の天気(晴れ,曇り,雨に分類)
    - 入力：9地点の現在時刻の気温,降水量,湿度,気圧
    - 正解率：約67%
"""

import sys, os

from enum import Enum
#import model
#from .. import model
from model import ModelRandomForest, ModelXgboost, ModelDnn
from runner import Runner2019

class ModelKind(Enum):
    RandomForest = 1    # ランダムフォレスト
    XGBoost = 2         # XGBoost
    DNN = 3             # DNN
    
##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    model_kind = ModelKind.ModelKind.XGBoost

    ##############################
    if model_kind == ModelKind.RandomForest:
        # ランダムフォレスト
        run_name = 'random_forest'
        model_params = { 
            'n_estimators' : 50, 'max_depth': 10, 'random_state':1,
            'model_dir' : 'model'
        }
        model = ModelRandomForest(run_name, model_params)
    
    ##############################
    elif model_kind == ModelKind.XGBoost:
        # XGBoost
        run_name = 'xgboost'
        xbg_param = {
            'max_depth': 5, 'eta': 0.1, 'subsample': 1.0, 
            'objective': 'multi:softmax', 'num_class': 3
        }
        model_parmas = {
            'xgb_param' : xbg_param, 'num_round' : 1000, 
            'early_stopping_rounds' : 40, 'verbose_eval' : 50,
            'model_dir' : 'model'
        }
        model = ModelXgboost(run_name, model_parmas)
    
    ##############################
    elif model_kind == ModelKind.DNN:
        # DNN
        run_name = 'dnn'
        model_parmas = {
            'units'                     : [32, 32],
            'dropout_rates'             : [0.5, 0.5],
            'learning_rate'             : 0.001,
            'kernel_initializer'        : 'he_normal',
            #'kernel_initializer'        : 'random_uniform',
            'max_epoch'                 : 10000,
            'epochs'                    : 50,
            'batch_size'                : 128,
            'validation_split'          : 0.1,
            'early_stopping_patience'   : 40,
            'model_dir'                 : 'model'
        }
        model = ModelDnn(run_name, model_parmas)
            
    # 気象庁の気象観測所のデータを用いた学習・評価・予測 実行クラス
    runner_param = {
        'base_dir'      :  os.getcwd(),
        'temp_dir'      : 'temp',
        'input_dir'     : 'input10_2019',
        'output_dir'    :  'output'
    }
    runner = Runner2019(run_name, model, runner_param)
    

    # クロスバリデーション実行
    runner.run_train_cv(4)
    
    # 学習実行
    #runner.run_train_all()
    
    # テストデータで予測を行う
    #runner.run_predict_all()
    
    