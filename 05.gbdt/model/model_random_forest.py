# coding: utf-8

from .abs_model import AbsModel
from sklearn.ensemble import RandomForestClassifier


class ModelRandomForest(AbsModel):
    
    def __init__(self, run_fold_name, params):
        # 抽象クラスのコンストラクタ
        super(ModelRandomForest, self).__init__(run_fold_name, params)
        
        # ランダムフォレストの学習モデルを生成する
        self.model = RandomForestClassifier(n_estimators=1000, max_depth=20, random_state=1)
        
    def train(self, train_x, train_y, validate_x=None, validate_y=None):
        self.model.fit(train_x, train_y)
        #pred_y = self.predict(validate_x)
        
        
    def predict(self, test_x):
        pred_y = self.model.predict(test_x)
        return pred_y
        
    def save_model(self):
        raise NotImplementedError()
        
    def load_model(self):
        raise NotImplementedError()
        
    def get_feature_importances(self):
        return self.model.feature_importances_
        
        