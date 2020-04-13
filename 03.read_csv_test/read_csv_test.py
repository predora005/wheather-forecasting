# coding: utf-8

import os
#import pandas as pd
import wfile
import wdfproc

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    # カレントディレクトリを取得する
    cwd = os.getcwd()

    # 地上気象データを取得する
    ground_dir = os.path.join(cwd, 'ground_weather')
    ground_df = wfile.get_ground_weather(ground_dir)
    ground_df.to_csv('ground.csv')
    
    # 高層気象データを取得する
    highrise_dir = os.path.join(cwd, 'highrise_weather')
    highrise_df = wfile.get_highrise_weather(highrise_dir)
    highrise_df.to_csv('highrise.csv')
    
    # 地上気象データからNaNが含まれる列を削る
    #print("==============================")
    #ground_df.info()
    #print("==============================")
    #ground_df = ground_df.replace('--', np.nan)
    #ground_df = ground_df.dropna(how='any', axis=1)
    #ground_df.info()
    #print("==============================")
    ground_df = wdfproc.drop_ground(ground_df)
    ground_df.to_csv('ground.csv')

    # 高層気象データからNaNが含まれる列を削る
    #print("==============================")
    #highrise_df.info()
    #print("==============================")
    #highrise_df = highrise_df.replace('--', np.nan)
    #highrise_df = highrise_df.dropna(how='any', axis=1)
    highrise_df = wdfproc.drop_higirise(highrise_df)
    highrise_df.info()
    #print("==============================")
    #print(type(highrise_df.isnull().any()))
    highrise_df.to_csv('highrise.csv')
