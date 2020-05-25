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

#from dtreeviz.trees import dtreeviz
#from sklearn.externals.six import StringIO
import pydotplus
from sklearn.tree import export_graphviz, plot_tree
#from sklearn.tree import DecisionTreeClassifier

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
    
    print(ground_df.info())

    return ground_df

##################################################
# 高層気象データ取得
##################################################
def get_highrise_weather():
    
    # カレントディレクトリを取得する
    cwd = os.getcwd()
    
    # 高層気象データを取得する
    highrise_dir = os.path.join(cwd, 'highrise_weather')
    highrise_df = wfile.get_highrise_weather(highrise_dir)
    highrise_df.to_csv('highrise.csv')
    
    print(highrise_df.info())
    
##################################################
# 学習データ作成
##################################################
def make_training_data(df, y_name):
    
    df = df.drop(columns=['時', '日付'])
    
    data_x = df.drop(columns=[y_name, ])
    data_y = df[y_name]

    # Xデータから末尾(最新時刻)のデータを削る
    data_x = data_x.iloc[:-1,]

    # Yデータから先頭(最旧時刻)のデータを削る
    data_y = data_y.iloc[1:,]

    train_x, test_x, train_y, test_y = train_test_split(data_x, data_y, shuffle=True)

    return train_x, train_y, test_x, test_y

##################################################
# 特徴量の重要度を表示する
##################################################
def show_importance_of_feature(model, train_x):
    
    importances = model.feature_importances_
    columns = train_x.columns
    feature_importances = pd.DataFrame(importances, index=train_x.columns, columns=['Importance'])
    feature_importances = feature_importances.sort_values(by='Importance', ascending=False)
    feature_importances.plot(kind='bar', figsize=(10,10))
    plt.savefig('feature_importances.png', bbox_inches='tight')

##################################################
# 正解率を表示する
##################################################
def print_accuracy(test_y, pred_y):
    
    # 正解率を表示する
    acc = accuracy_score(test_y, pred_y)
    print('Score:{0:.4f}'.format(acc))
    
    idx_sunny = np.where(test_y.values == 0)[0]
    acc_sunnny = accuracy_score(test_y.iloc[idx_sunny], pred_y[idx_sunny])
    print('Score(sunny):{0:.4f}'.format(acc_sunnny))
    
    idx_cloudy = np.where(test_y.values == 1)[0]
    acc_cloudy= accuracy_score(test_y.iloc[idx_cloudy], pred_y[idx_cloudy])
    print('Score(cloudy):{0:.4f}'.format(acc_cloudy))
    
    idx_rain = np.where(test_y.values == 2)[0]
    acc_rain= accuracy_score(test_y.iloc[idx_rain], pred_y[idx_rain])
    print('Score(rain):{0:.4f}'.format(acc_rain))
    

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    # 地上気象データを取得する
    df = get_ground_weather()
    
    # 高層気象データを取得する
    df2 = get_highrise_weather()
    
    # NaNを置換する
    df = df.fillna(-9999)
    
    # 学習データ・テスト用データ作成
    train_x, train_y, test_x, test_y = make_training_data(df, 'Mito_天気')
    
    # ランダムフォレストの学習モデルを生成する
    #model = DecisionTreeClassifier(max_depth=20, random_state=1)
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=1)
    
    # 学習データで学習を行う
    model.fit(train_x, train_y)
    
    # 特徴量の重要度を可視化する
    show_importance_of_feature(model, train_x)
    
    # テストデータで予測を行う
    pred_y = model.predict(test_x)
    
    # 正解率を表示する
    print_accuracy(test_y, pred_y)
    
    #viz = dtreeviz(
    #    model.estimators_[0],
    #    train_x, 
    #    train_y,
    #    target_name='weather',
    #    feature_names=train_x.columns,
    #    class_names=['Sunny', 'Cloud', 'Rain']
    #)
    #viz.save("tree_dtreeviz.svg")
    
    #dot_data = StringIO()
    #tree.export_graphviz(
    #    model.estimators_[0], 
    #    out_file=dot_data,  
    #    feature_names=train_x.columns,
    #    class_names=['Sunny', 'Cloud', 'Rain'],  
    #    filled=True, rounded=True, special_characters=True
    #)
    #graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    #graph.write_png("tree_graphviz.png") 
    
    dot_data = export_graphviz(
        model.estimators_[0], 
        #model,
        feature_names=train_x.columns,
        class_names=['Sunny', 'Cloud', 'Rain'],  
        filled=True, 
        rounded=True)
    graph = pydotplus.graph_from_dot_data( dot_data )
    graph.write_png('tree_graphviz.png')
    
    fig = plt.figure(figsize=(100, 50))
    ax = fig.add_subplot()
    plot_tree(
        model.estimators_[0], 
        #model,
        feature_names=train_x.columns,
        ax=ax, 
        class_names=['Sunny', 'Cloud', 'Rain'],
        filled=True
    )
    plt.savefig('tree_plt.png', bbox_inches='tight')
    
