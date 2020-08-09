# coding: utf-8

from .abs_model import AbsModel

import os
import xgboost as xgb
import matplotlib.pyplot as plt

##################################################
# XGBoost
##################################################
class ModelXgboost(AbsModel):
    """ XGBoost
        
    Attributes:
        run_fold_name (string)  : ランとfoldを組み合わせた名称
        params (dict)           : パラメータ
    """
    
    ##################################################
    # コンストラクタ
    ##################################################
    def __init__(self, run_fold_name, params):
        """ コンストラクタ
        
        Args:
            run_fold_name(string)   : ランとfoldを組み合わせた名称
            params(dict)            : パラメータ
        """
        
        # 抽象クラスのコンストラクタ
        super().__init__(run_fold_name, params)
        
        # ディレクトリ名
        self._model_dir = self._params['model_dir']
        
        self._model = None
        
    ##################################################
    # 学習
    ##################################################
    def train(self, train_x, train_y, validate_x=None, validate_y=None):
        """ 学習
        
        Args:
            train_x(DataFrame)  : 学習データ(入力)
            train_y(DataFrame)  : 学習データ(出力)
        """
        dtrain = xgb.DMatrix(train_x, label=train_y)
        
        if (validate_x is not None) and (validate_y is not None):
            dvalid = xgb.DMatrix(validate_x, label=validate_y)
            evallist = [(dtrain, 'train'), (dvalid, 'eval')]
        else:
            evallist = [(dtrain, 'train')]
        
        xgb_param = self._params['xgb_param']
        num_round = self._params['num_round']
        early_stopping_rounds = self._params['early_stopping_rounds']
        verbose_eval = self._params['verbose_eval']
        
        self._model = xgb.train(
            xgb_param, dtrain, num_round, evallist, 
            early_stopping_rounds = early_stopping_rounds, 
            verbose_eval = verbose_eval
        )

    ##################################################
    # 予測
    ##################################################
    def predict(self, test_x):
        """ 予測
        
        Args:
            test_x(DataFrame)   : テストデータ(入力)

        Returns:
            DataFrame : テストデータ(出力)
        """
        dtest = xgb.DMatrix(test_x)
        pred_y = self._model.predict(dtest)
        
        print('Best Score:{0:.4f}, Iteratin:{1:d}, Ntree_Limit:{2:d}'.format(
                self._model.best_score, self._model.best_iteration, 
                self._model.best_ntree_limit))
        
        return pred_y
        
    ##################################################
    # モデルをファイルに保存する
    ##################################################
    def save_model(self):
        """ モデルをファイルに保存する
        """
        os.makedirs(self._model_dir, exist_ok=True)
        file_name = "{0:s}.model".format(self._run_fold_name)
        file_path = os.path.join(self._model_dir, file_name)
        self._model.save_model(file_path)
        
    ##################################################
    # モデルをファイルからロードする
    ##################################################
    def load_model(self):
        """ モデルをファイルからロードする
        """
        file_name = "{0:s}.model".format(self._run_fold_name)
        file_path = os.path.join(self._model_dir, file_name)
        self._model = xgb.Booster({'nthread': 1})
        self._model.load_model(file_path)

    ##################################################
    # 特徴量の重要度をプロットする
    ##################################################
    def plot_feature_importances(self, filepath):
        xgb.plot_importance(self._model)
        plt.savefig(filepath)
        #return self._model.feature_importances_
        
    ##################################################
    # Graphvizのグラフをファイルに出力する
    ##################################################
    def export_graphviz(self, filepath):
        #xgb.to_graphviz(self._model, num_trees=1)
        #xgb.plot_tree(bst, num_trees=2, ax=axes[0])
        
        xgb.plot_tree(self._model, num_trees=1)
        plt.savefig(filepath)
        