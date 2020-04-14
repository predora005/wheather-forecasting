# coding: utf-8

import os
import wfile
import wdfproc

##################################################
# 地上気象データ取得
##################################################
def get_ground_weather():
    
    # カレントディレクトリを取得する
    cwd = os.getcwd()

    # 地上気象データを取得する
    ground_dir = os.path.join(cwd, 'ground_weather')
    ground_df = wfile.get_ground_weather(ground_dir)
    
    # 地上気象データからNaNが含まれる列を削る
    ground_df = wdfproc.drop_ground(ground_df)
    
    # 風速・風向きを数値に変換する
    ground_df = wdfproc.convert_wind(ground_df)
    ground_df.to_csv('ground.csv')
    

##################################################
# 高層気象データ取得
##################################################
def get_highrise_weather():
    
    # 高層気象データを取得する
    highrise_dir = os.path.join(cwd, 'highrise_weather')
    highrise_df = wfile.get_highrise_weather(highrise_dir)
    highrise_df.to_csv('highrise.csv')
    

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    get_ground_weather()
    
