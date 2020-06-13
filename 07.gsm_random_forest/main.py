# coding: utf-8

from model import ModelRandomForest, ModelXgboost
from runner import GsmForecastRunner
#from sklearn.model_selection import StratifiedKFold

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    # ランダムフォレスト
    run_name = 'Random Forest'
    params = { 'n_estimators' : 2000, 'max_depth': 30, 'random_state':1 }
    model = ModelRandomForest(run_name, params)
    
    # XGBoost
    #run_name = 'XGBoost'
    #xbg_param = {
    #    'max_depth': 4, 'eta': 0.05, 'subsample': 0.9, 
    #    'objective': 'multi:softmax', 'num_class': 4
    #}
    #parmas = {
    #    'xgb_param' : xbg_param, 'num_round' : 10000, 
    #    'early_stopping_rounds' : 10, 'verbose_eval' : 10
    #}
    #model = ModelXgboost(run_name, parmas)
        
    # Runner生成
    #runner = WeatherStationForecastRunner(run_name, model, None)
    runner = GsmForecastRunner(run_name, model, None)
    
    # クロスバリデーション実行
    runner.run_train_cv()
    
    # 学習実行
    runner.run_train_all()
    
    # テストデータで予測を行う
    runner.run_predict_all()
    
    