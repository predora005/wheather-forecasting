# coding: utf-8

from model import ModelRandomForest
from runner import GsmForecastRunner
from sklearn.model_selection import StratifiedKFold

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    run_name = 'Random Forest'
    
    # モデル生成
    model = ModelRandomForest(run_name, None)
        
    # Runner生成
    #runner = WeatherStationForecastRunner(run_name, model, None)
    runner = GsmForecastRunner(run_name, model, None)
    
    # クロスバリデーション実行
    #runner.run_train_cv()
    
    # 学習実行
    runner.run_train_all()
    
    # テストデータで予測を行う
    runner.run_predict_all()
    
    