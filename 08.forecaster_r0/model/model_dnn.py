# coding: utf-8

from .abs_model import AbsModel

import os
import numpy as np
import keras
from keras import optimizers
from keras.models import Sequential, load_model
from keras.layers import Dense, Activation, Dropout, LeakyReLU
from sklearn.model_selection import train_test_split
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
        
        # ディレクトリ名
        self._model_dir = self._params['model_dir']
        
        self._model = None
        
    ##################################################
    # モデル作成
    ##################################################
    def _create_model(self, data_x, data_y):
        
        input_dim = data_x.shape[1]
        units = self._params['units']
        dropout_rates = self._params['dropout_rates']
        label_num = self._params['label_num']
        learning_rate = self._params['learning_rate']
        kernel_initializer = self._params['kernel_initializer']
            
        # DNNの学習モデルを生成する
        model = Sequential()
        model.add(Dense(units[0], input_dim=input_dim, kernel_initializer=kernel_initializer))
        model.add(LeakyReLU())
        model.add(Dropout(rate=dropout_rates[0]))
        for i in range(1, len(units)):
            model.add(Dense(units[i], kernel_initializer=kernel_initializer))
            model.add(LeakyReLU())
            model.add(Dropout(rate=dropout_rates[i]))
            
        model.add(Dense(label_num))
        model.add(Activation('softmax'))
        
        model.summary()
        
        # 最適化アルゴリズムを設定する
        #optimizer = optimizers.SGD(lr=learning_rate)
        optimizer = optimizers.Adam(lr=learning_rate)
        model.compile(
            optimizer=optimizer,
            loss='categorical_crossentropy',
            metrics=['accuracy'])
        
        self._model = model
        
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
        
        # パラメータを取り出す
        max_epoch = self._params['max_epoch']
        epochs = self._params['epochs']
        batch_size = self._params['batch_size']
        early_stopping_patience = self._params['early_stopping_patience']
        
        # ラベルをOne-Hot Labelに変換する
        label_num = self._params['label_num']
        train_y_onehot = keras.utils.to_categorical(train_y, num_classes=label_num)
        
        # バリデーション用のパラメータ設定
        if (validate_x is not None) and (validate_y is not None):
            vy_onehot = keras.utils.to_categorical(validate_y, num_classes=label_num)
            validation_data = [validate_x, vy_onehot] 
        else:
            validation_split = self._params['validation_split']
            train_x, validate_x, train_y_onehot, vy_onehot = train_test_split(
                train_x, train_y_onehot, shuffle=True, test_size=validation_split)
            validation_data = [validate_x, vy_onehot]

        # Early Stopping
        #   patience: 指定した回数改善しなければ終了
        early_stopping = keras.callbacks.EarlyStopping(
            monitor='val_loss', min_delta=0, patience=early_stopping_patience, 
            verbose=1, mode='auto')
        
        # self._max_epoch回数分、学習を実行する
        epoch = 0
        num_loop = int(np.ceil(max_epoch / epochs))
        for i in range(num_loop):
            
            # 学習
            self._model.fit(
                train_x, train_y_onehot, 
                epochs=epochs, batch_size=batch_size, 
                shuffle=True, verbose=0, callbacks=[early_stopping], 
                #validation_data=validation_data,
                #validation_split=validation_split
            )
            
            # epochを更新する
            epoch = epoch + epochs
            
            # 損失値と正解率を表示する
            score = self._model.evaluate(train_x, train_y_onehot, verbose=0)
            loss, acc = score[0], score[1]
            if validation_data is not None:
                score = self._model.evaluate(validation_data[0], validation_data[1], verbose=0)
                val_loss, val_acc = score[0], score[1]
            else:
                val_loss, val_acc = 0, 0
                
            print('%07d : loss=%f, acc=%f val_loss=%f, val_acc=%f' % 
                    (epoch, loss, acc, val_loss, val_acc))
                    
            # Early Stoppingが行われていればループを離脱する
            if early_stopping.stopped_epoch > 0:
                break
            
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
        os.makedirs(self._model_dir, exist_ok=True)
        file_name = "{0:s}.h5".format(self._run_fold_name)
        file_path = os.path.join(self._model_dir, file_name)
        self._model.save(file_path)
        
    ##################################################
    # モデルをファイルからロードする
    ##################################################
    def load_model(self):
        """ モデルをファイルからロードする
        """
        file_name = "{0:s}.h5".format(self._run_fold_name)
        file_path = os.path.join(self._model_dir, file_name)
        self._model = load_model(file_path)
        
