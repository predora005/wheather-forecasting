# coding: utf-8

from model import ModelRandomForest, ModelXgboost
from runner import GsmForecastRunner
#from sklearn.model_selection import StratifiedKFold

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    run_name = 'Random Forest'
    model = ModelRandomForest(run_name, None)
    
    # モデル生成
    #run_name = 'XGBoost'
    #xbg_param = {
    #    'max_depth': 4, 'eta': 0.05, 'subsample': 0.9, 
    #    'objective': 'multi:softmax', 'num_class': 4
    #}
    #model = ModelXgboost(run_name, xbg_param)
        
    # Runner生成
    #runner = WeatherStationForecastRunner(run_name, model, None)
    runner = GsmForecastRunner(run_name, model, None)
    
    # クロスバリデーション実行
    runner.run_train_cv()
    
    # 学習実行
    runner.run_train_all()
    
    # テストデータで予測を行う
    runner.run_predict_all()
    
    