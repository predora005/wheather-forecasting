# coding: utf-8

from .abs_model import AbsModel
from sklearn.ensemble import RandomForestClassifier

##################################################
# ランダムフォレスト
##################################################
class ModelRandomForest(AbsModel):
    """ランダムフォレスト
        
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
        
        # ランダムフォレストの学習モデルを生成する
        self._params = params
        n_estimators = self._params['n_estimators']
        max_depth = self._params['max_depth']
        random_state = self._params['random_state']
        self._model = RandomForestClassifier(
            n_estimators = n_estimators, 
            max_depth = max_depth, 
            random_state = random_state
        )
        
    ##################################################
    # 学習
    ##################################################
    def train(self, train_x, train_y, validate_x=None, validate_y=None):
        """ 学習
        
        Args:
            train_x(DataFrame)  : 学習データ(入力)
            train_y(DataFrame)  : 学習データ(出力)
        """
        epoch = 0
        for i in range(100):
            model.fit(
                train_input, train_label, 
                epochs=100, batch_size=16, shuffle=False, verbose=0)
            score = model.evaluate(test_input, test_label, verbose=0)
            
            epoch = epoch + 100
            print('%07d : loss=%f, acc=%f' % (epoch, score[0], score[1]))
            #print(model.metrics_names['accuracy'])
        self._model.fit(train_x, train_y)
        #pred_y = self.predict(validate_x)
        
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
        pred_y = self._model.predict(test_x)
        return pred_y
        
    ##################################################
    # モデルをファイルに保存する
    ##################################################
    def save_model(self):
        """ モデルをファイルに保存する
        """
        raise NotImplementedError()
        
    ##################################################
    # モデルをファイルからロードする
    ##################################################
    def load_model(self):
        """ モデルをファイルからロードする
        """
        raise NotImplementedError()
        
    ##################################################
    # 特徴量の重要度を返す
    ##################################################
    def get_feature_importances(self):
        return self._model.feature_importances_
        
    ##################################################
    # 推定器を返す
    ##################################################
    def get_estimators(self):
        return self._model.estimators_
        
        