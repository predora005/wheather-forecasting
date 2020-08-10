# coding: utf-8

from abc import ABCMeta, abstractmethod

##################################################
# 学習・評価・予測 実行クラスの基底クラス
##################################################
class AbsRunner(metaclass=ABCMeta):
    """学習・評価・予測 実行クラス
        
    Attributes:
        run_name (string)   : ランの名称
        model (AbsModel)    : モデル
        params (dict)       : パラメータ
    """
    ##################################################
    # コンストラクタ
    ##################################################
    def __init__(self, run_name, model, params):
        self._run_name = run_name
        self._model = model
        self._params = params
        
        # 各種フラグ
        self._is_data_loaded = False # データ読み込み済みフラグ
        self._is_trained_all = False # 全データで学習済みフラグ
        
        # 全データ
        self._whole_x = None
        self._whole_y = None
        
        # 学習・予測用データ
        self._train_x = None
        self._train_y = None
        self._test_x = None
        self._test_y = None
        
    ##################################################
    # foldを指定して学習・評価を行う
    ##################################################
    @abstractmethod
    def run_train_fold(self, fold):
        raise NotImplementedError()
        
    ##################################################
    # クロスバリデーションで学習・評価を行う
    ##################################################
    @abstractmethod
    def run_train_cv(self, fold_splits):
        raise NotImplementedError()
    
    ##################################################
    # クロスバリデーションで学習した
    # 各foldモデルの平均で予測を行う
    ##################################################
    @abstractmethod
    def run_predict_cv(self):
        raise NotImplementedError()
        
    ##################################################
    # 学習データ全てを使用して、学習を行う
    ##################################################
    @abstractmethod
    def run_train_all(self):
        raise NotImplementedError()
    
    ##################################################
    # 学習データ全てを学習したモデルで、
    # テストデータの予測を行う
    ##################################################
    @abstractmethod
    def run_predict_all(self):
        raise NotImplementedError()
        
        