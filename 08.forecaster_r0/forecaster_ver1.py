# coding: utf-8

import os
from enum import Enum
from model import ModelRandomForest, ModelXgboost, ModelDnn
from runner import WeatherStationForecastRunner2020Ver1, GsmForecastRunner

class ModelKind(Enum):
    RandomForest = 1    # ランダムフォレスト
    XGBoost = 2         # XGBoost
    DNN = 3             # DNN
    
class RunnerKind(Enum):
     WeatherStationForecast = 1 # WeatherStationForecast
     GsmForecastRunner = 2      # GsmForecast

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    model_kind = ModelKind.XGBoost
    runner_kind = RunnerKind.WeatherStationForecast

    ##############################
    if model_kind == ModelKind.RandomForest:
        # ランダムフォレスト
        run_name = 'random_forest'
        model_params = { 
            'n_estimators' : 2000, 'max_depth': 30, 'random_state':1,
            'model_dir' : 'model'
        }
        model = ModelRandomForest(run_name, model_params)
    
    ##############################
    elif model_kind == ModelKind.XGBoost:
        # XGBoost
        run_name = 'xgboost'
        xbg_param = {
            'max_depth': 5, 'eta': 0.05, 'subsample': 1.0, 
            'objective': 'multi:softmax', 'num_class': 4
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
            'units'                     : [1024, 256],
            'dropout_rates'             : [0.5, 0.5],
            'learning_rate'             : 0.0001,
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
            
    ##############################
    if runner_kind == RunnerKind.WeatherStationForecast:
        # 気象庁の気象観測所のデータを用いた学習・評価・予測 実行クラス
        runner_param = {
            'base_dir'      :  os.getcwd(),
            'temp_dir'      : 'temp',
            'input_dir'     : 'input2',
            'output_dir'    :  'output',
            'class_names'   : ['Sunny', 'Cloud', 'Rain'],
            'label_name'    : 'Mito_天気'
        }
        runner = WeatherStationForecastRunner2020Ver1(run_name, model, runner_param)
    
    ##############################
    elif runner_kind == RunnerKind.GsmForecastRunner:
        # GSMデータを用いた学習・評価・予測 実行クラス
        runner_param = {
            'base_dir'              : os.getcwd(),
            'temp_dir'              : 'temp',
            'input_dir'             : 'input6',
            'input2_dir'            : 'input2',
            'output_dir'            :  'output',
            'gsm_thinout_interval'  : (4,4),
            'weather_convert_mode'  : 'default',
            'class_names'           : ['Sunny', 'Cloud', 'Rain', 'Other'],
            #'weather_convert_mode'  : 'rain_or_not',
            #'class_names'           : ['Except for Rain', 'Rain'],
            'label_name'            : 'Mito_天気'
            
        }
        runner = GsmForecastRunner(run_name, model, runner_param)
    
    # クロスバリデーション実行
    runner.run_train_cv(4)
    
    # 学習実行
    runner.run_train_all()
    
    # テストデータで予測を行う
    runner.run_predict_all()
    
    