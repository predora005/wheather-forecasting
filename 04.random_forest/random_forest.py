# coding: utf-8

import os
import wfile
import wdfproc
import numpy as np
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
    
    
    #ground_df = ground_df.astype({'Chichibu_降水量(mm)': np.float32})
    #print(ground_df.info())
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
    
    train_y = df[y_name]
    
    train_y_dict = {}
    
    #train_
    
##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    df = get_ground_weather()
    
    #train_x, train_y = make_training_data(df, 'Mito_天気')

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