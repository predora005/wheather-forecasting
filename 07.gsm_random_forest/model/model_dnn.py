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
        
        input_dim = self._params['input_dim']
        label_num = self._params['label_num']
        units = self._params['units']
        learning_rate = self._params['learning_rate']
        
        # DNNの学習モデルを生成する
        model = Sequential()
        model.add(Dense(units[0], input_dim=input_data_dim))
        model.add(Activation('relu'))
        for i in range(1, len(units.len):
            model.add(Dense(units[i]))
            model.add(Activation('relu'))
        model.add(Dense(label_num))
        model.add(Activation('softmax'))
        
        optimizer = optimizers.Adam(lr=learning_rate)
        model.compile(
            optimizer=optimizer,
            loss='categorical_crossentropy',
            metrics=['accuracy'])
        
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
        
        label_num = self._params['label_num']
        one_hot_labels = keras.utils.to_categorical(train_y, num_classes=label_num)
        
        epoch = 0
        for i in range(100):
            model.fit(
                train_input, train_label, 
                epochs=100, batch_size=16, shuffle=False, verbose=0)

            score = model.evaluate(test_input, test_label, verbose=0)
            loss = score[0]
            acc = score[1]
            print('%07d : loss=%f, acc=%f' % (epoch, loss, acc))            
            
            epoch = epoch + 100
            print('%07d : loss=%f, acc=%f' % (epoch, score[0], score[1]))
            #print(model.metrics_names['accuracy'])
        
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
        pred_y = None
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
        
