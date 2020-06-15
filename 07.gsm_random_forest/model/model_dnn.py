# coding: utf-8

from .abs_model import AbsModel
import keras
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense, Activation
#import matplotlib.pyplot as plt

##################################################
# DNN
##################################################
class ModelDnn(AbsModel):
    """ DNN
        
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
        
        self._params = params

        self._dnn_units = self._params['units']
        self._learning_rate = self._params['learning_rate']
        self._max_epoch = self._params['max_epoch']
        self._epochs = self._params['epochs']
        self._batch_size = self._params['batch_size']
        
        #label_num = self._params['label_num']
        #learning_rate = self._params['learning_rate']
        
        self._model = None
        
    ##################################################
    # モデル作成
    ##################################################
    def _create_model(self, data_x, data_y):
        
        # モデル未作成の場合
        #if self._is_model_crated == False:
            
        input_dim = data_x.shape[1]
        label_num = self._params['label_num']
        learning_rate = self._params['learning_rate']
        units = self._dnn_units
            
        # DNNの学習モデルを生成する
        model = Sequential()
        model.add(Dense(units[0], input_dim=input_dim))
        model.add(Activation('relu'))
        for i in range(1, len(units)):
            model.add(Dense(units[i]))
            model.add(Activation('relu'))
            
        model.add(Dense(label_num))
        model.add(Activation('softmax'))
        
        # 最適化アルゴリズムを設定する
        optimizer = optimizers.Adam(lr=learning_rate)
        model.compile(
            optimizer=optimizer,
            loss='categorical_crossentropy',
            metrics=['accuracy'])
        
        self._model = model
        
            #self._is_model_crated = True

    ##################################################
    # 学習
    ##################################################
    def train(self, train_x, train_y, validate_x=None, validate_y=None):
        """ 学習
        
        Args:
            train_x(DataFrame)  : 学習データ(入力)
            train_y(DataFrame)  : 学習データ(出力)
        """
        
        # モデルを生成する
        self._create_model(train_x, train_y)
        
        # ラベルをOne-Hot Labelに変換する
        label_num = self._params['label_num']
        label_onehot = keras.utils.to_categorical(train_y, num_classes=label_num)
        
        # self._max_epoch回数分、学習を実行する
        epoch = 0
        num_loop = int(numpy.ceil(self._max_epoch / self._epochs))
        for i in range(num_loop):
            
            # 学習
            self._model.fit(
                train_x, label_onehot, 
                epochs=self._epochs, batch_size=self._batch_size, shuffle=False, verbose=0)
            
            # epochを更新する
            epoch = epoch + self._epochs
            
            # 損失値と正解率を表示する
            score = self._model.evaluate(train_x, label_onehot, verbose=0)
            loss = score[0]
            acc = score[1]
            print('%07d : loss=%f, acc=%f' % (epoch, loss, acc))            
            
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
        
