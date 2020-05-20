# coding: utf-8

import os
import wfile
import wdfproc
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.font_manager._rebuild() #キャッシュの削除
plt.rcParams['font.family'] = 'IPAGothic' # インストールしたフォントを指定

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
#from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score

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
    train_data, test_data = train_test_split(df, shuffle=True)
    
    train_x = train_data.drop(columns=[y_name, ])
    train_y = train_data[y_name]
    
    test_x = test_data.drop(columns=[y_name])
    test_y = test_data[y_name]
    
    # Xデータから末尾(最新時刻)のデータを削る
    train_x = train_x.iloc[:-1,]
    test_x = test_x.iloc[:-1,]
    
    # Yデータから先頭(最急時刻)のデータを削る
    train_y = train_y.iloc[1:,]
    test_y = test_y.iloc[1:,]
    
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
    model = RandomForestClassifier(n_estimators=5000, max_depth=10, random_state=1)
    
    # 学習データで学習を行う
    model.fit(train_x, train_y)
    
    # 特徴量の重要度を可視化する
    importances = model.feature_importances_
    columns = train_x.columns
    feature_importances = pd.DataFrame(importances, index=train_x.columns, columns=['Importance'])
    feature_importances = feature_importances.sort_values(by='Importance', ascending=False)
    feature_importances.plot(kind='bar', figsize=(10,10))
    plt.savefig('test.png', bbox_inches='tight')
    
    # テストデータで予測を行う
    pred_y = model.predict(test_x)
    
    # 正解率を表示する
    acc = accuracy_score(test_y, pred_y)
    print('Score:{0:.4f}'.format(acc))
    
    #print(test_y)
    #idx_sunny = test_y[test_y == 0]
    idx_sunny = np.where(test_y.values == 0)[0]
    #print(idx_sunny)
    #print(test_y.iloc[idx_sunny])
    #print(pred_y[idx_sunny])
    acc_sunnny = accuracy_score(test_y.iloc[idx_sunny], pred_y[idx_sunny])
    print('Score(sunny):{0:.4f}'.format(acc_sunnny))
    
    idx_cloud = np.where(test_y.values == 1)[0]
    #print(idx_cloud)
    #print(test_y.iloc[idx_cloud])
    #print(pred_y[idx_cloud])
    acc_cloud= accuracy_score(test_y.iloc[idx_cloud], pred_y[idx_cloud])
    print('Score(cloud):{0:.4f}'.format(acc_cloud))
    
    idx_rainy = np.where(test_y.values == 2)[0]
    print(idx_rainy)
    print(test_y.iloc[idx_rainy])
    print(pred_y[idx_rainy])
    acc_rainy= accuracy_score(test_y.iloc[idx_rainy], pred_y[idx_rainy])
    print('Score(rainy):{0:.4f}'.format(acc_rainy))
    
    