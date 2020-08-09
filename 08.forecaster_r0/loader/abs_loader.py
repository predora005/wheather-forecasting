# coding: utf-8

import os
from abc import ABCMeta, abstractmethod

##################################################
# データロードクラスの基底クラス
##################################################
class AbsLoader(metaclass=ABCMeta):
    """データロードクラスの基底クラス
        
    Attributes:
        _base_dir (string)      : ベースディレクトリ
        _temp_dirname (string)  : 一時ディレクトリ名
        _input_dirname (string) : 入力ディレクトリ名
        _label_name (string)     : 正解データのラベル名
    """
    
    ##################################################
    # コンストラクタ
    ##################################################
    def __init__(self, base_dir, temp_dirname, input_dirname, label_name):
        self._base_dir = base_dir
        self._temp_dirname = temp_dirname
        self._input_dirname = input_dirname
        self._label_name = label_name
        
        # ワーク用ディレクトリをセットする
        self._temp_dir = os.path.join(self._base_dir, self._temp_dirname)
        
        # 入力データ格納ディレクトリをセットする
        self._input_dir = os.path.join(self._base_dir, self._input_dirname)
        
    
    ##################################################
    # データをロードする
    ##################################################
    @abstractmethod
    def load(self, reload):
        raise NotImplementedError()
        
