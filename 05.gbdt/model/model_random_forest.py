# coding: utf-8

from .abs_model import AbsModel
from sklearn.ensemble import RandomForestClassifier

##################################################
# ランダムフォレスト
##################################################
class ModelRandomForest(AbsModel):
    """ランダムフォレスト
        
    Attributes:
        属性の名前 (属性の型): 属性の説明
        属性の名前 (:obj:`属性の型`): 属性の説明.
    """
    
    ##################################################
    # コンストラクタ
    ##################################################
    def __init__(self, run_fold_name, params):
        
        # 抽象クラスのコンストラクタ
        super(ModelRandomForest, self).__init__(run_fold_name, params)
        
        # ランダムフォレストの学習モデルを生成する
        self.model = RandomForestClassifier(n_estimators=1000, max_depth=20, random_state=1)
        
    ##################################################
    # 学習
    ##################################################
    def train(self, train_x, train_y, validate_x=None, validate_y=None):
        self.model.fit(train_x, train_y)
        #pred_y = self.predict(validate_x)
        
    ##################################################
    # 予測
    ##################################################
    def predict(self, test_x):
        pred_y = self.model.predict(test_x)
        return pred_y
        
    ##################################################
    # モデルをファイルに保存する
    ##################################################
    def save_model(self):
        raise NotImplementedError()
        
    ##################################################
    # モデルをロードする
    ##################################################
    def load_model(self):
        raise NotImplementedError()
        
    ##################################################
    # 特徴量の重要度を返す
    ##################################################
    def get_feature_importances(self):
        return self.model.feature_importances_
        
    ##################################################
    # 推定器を返す
    ##################################################
    def get_estimators(self):
        return self.model.estimators
        
        