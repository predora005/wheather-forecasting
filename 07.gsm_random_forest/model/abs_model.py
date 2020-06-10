# coding: utf-8

from abc import ABCMeta, abstractmethod

##################################################
# 学習モデルの基底クラス
##################################################
class AbsModel(metaclass=ABCMeta):
    """学習モデルの基底クラス
        
    Attributes:
        run_fold_name (string)  : ランとfoldを組み合わせた名称
        params (dict)           : パラメータ
    """
    
    ##################################################
    # コンストラクタ
    ##################################################
    def __init__(self, run_fold_name, params):
        self._run_fold_name = run_fold_name
        self._params = params

    ##################################################
    # 学習
    ##################################################
    @abstractmethod
    def train(self, train_x, train_y, validate_x, validate_y):
        raise NotImplementedError()
        
    ##################################################
    # 予測
    ##################################################
    @abstractmethod
    def predict(self, test_x):
        raise NotImplementedError()
        
    ##################################################
    # モデルをファイルに保存する
    ##################################################
    @abstractmethod
    def save_model(self):
        raise NotImplementedError()
        
    ##################################################
    # モデルをファイルからロードする
    ##################################################
    @abstractmethod
    def load_model(self):
        raise NotImplementedError()
        
        