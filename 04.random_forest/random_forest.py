# coding: utf-8

import os
import wfile
import wdfproc
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score

##################################################
# 地上気象データ取得
##################################################
def get_ground_weather():
    
    # カレントディレクトリを取得する
    cwd = os.getcwd()

    # 地上気象データを取得する
    ground_dir = os.path.join(cwd, 'ground_weather')
    ground_df = wfile.get_ground_weather(ground_dir)
    ground_df.to_csv('ground1.csv')
    
    # 地上気象データからNaNが含まれる列を削る
    ground_df = wdfproc.drop_ground(ground_df)
    ground_df.to_csv('ground2.csv')
    
    # 風速・風向きを数値に変換する
    ground_df = wdfproc.convert_wind_to_vector(ground_df)
    ground_df.to_csv('ground3.csv')
    
    # 天気を数値に変換する
    ground_df = wdfproc.convert_weather_to_interger(ground_df)
    ground_df.to_csv('ground4.csv')
    
    # 雲量を浮動小数点数に変換する
    ground_df = wdfproc.convert_cloud_volume_to_float(ground_df)
    ground_df.to_csv('ground5.csv')
    
    # 天気を指定した境界値で分類する
    ground_df = wdfproc.classify_weather(ground_df)
    ground_df.to_csv('ground6.csv')
    
    # 浮動小数点数を32ビットに変換する
    ground_df = wdfproc.type_to_float32(ground_df)
    ground_df.to_csv('ground7.csv')
    
    #ground_df = ground_df.astype({'Chichibu_降水量(mm)': np.float32})
    print(ground_df.info())
    #print(ground_df['Chichibu_降水量(mm)'])
    
    return ground_df

##################################################
# 高層気象データ取得
##################################################
def get_highrise_weather():
    
    # 高層気象データを取得する
    highrise_dir = os.path.join(cwd, 'highrise_weather')
    highrise_df = wfile.get_highrise_weather(highrise_dir)
    highrise_df.to_csv('highrise.csv')
    

##################################################
# 学習データ作成
##################################################
def make_training_data(df, y_name):
    
    df = df.drop(columns=['時', '日付'])
    train_data, test_data = train_test_split(df)
    
    #train_data.info()
    
    train_x = train_data.drop(columns=[y_name, ])
    train_y = train_data[y_name]
    
    test_x = test_data.drop(columns=[y_name])
    test_y = test_data[y_name]
    
    return train_x, train_y, test_x, test_y
    

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    # 地上気象データを取得する
    df = get_ground_weather()
    
    # NaNを置換する
    df = df.fillna(-9999)
    
    # 学習データ・テスト用データ作成
    train_x, train_y, test_x, test_y = make_training_data(df, 'Mito_天気')
    
    # ランダムフォレストの学習モデルを生成する
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
    model.fit(train_x, train_y)
    
    #font = {"family":"IPAexGothic"}
    #matplotlib.rc('font',**font)
    #matplotlib.font_manager._rebuild()
    mpl.font_manager._rebuild() #キャッシュの削除
    plt.rcParams['font.family'] = 'IPAGothic' # インストールしたフォントを指定
    
    importances = model.feature_importances_
    columns = train_x.columns
    feature_importances = pd.DataFrame(importances, index=train_x.columns, columns=['Importance'])
    feature_importances = feature_importances.sort_values(by='Importance', ascending=False)
    #fig = plt.figure(figsize=(8.0, 6.0))
    feature_importances.plot(kind='bar', figsize=(10,10))
    plt.savefig('test.png')
    print(mpl.matplotlib_fname()) #設定ファイルを表示（matplotlibrcは後で作ります）
    print(mpl.rcParams['font.family']) #現在使用しているフォントを表示
    print(mpl.get_configdir()) #設定ディレクトリを表示
    print(mpl.get_cachedir()) #キャッシュディレクトリを表示
    print(mpl.font_manager.findSystemFonts())
    #print(matplotlib.font_manager.ttflist)
    #print(matplotlib.rcParams['font.family']) #現在使用しているフォントを表示
    
    # Trainning with cross validation and and score calculation
    #model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
    #kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=1)
    #result = cross_val_score(model, train_x, train_y, cv=kf, scoring='accuracy')
    #print('Score:{0:.4f}'.format(result.mean()))

    # Evaluation of features
    #model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
    #model.fit(train_x, train_y)

    #importances = model.feature_importances_
    #columns = train_x.columns
    
    #feature_importances = pd.DataFrame(importances, index=train_x.columns, columns=['Importance'])
    #feature_importances = feature_importances.sort_values(by='Importance', ascending=False)
    #feature_importances.plot.bar()