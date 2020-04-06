# coding: utf-8

from scraping import HighriseWeatherDataScraping
from scraping import GroundWeatherDataScraping

import os
import datetime
import time

##################################################
# 高層の気象データをスクレイピングする
##################################################
def scrape_high_rise_weather_data():
    
    # 年月日・時刻・地点情報
    year = 2017
    month = 1
    day = 1
    hour = 9
    point = 47646   # 館野
    
    # 地点ごとにディレクトリ作成
    dirpath = str(point)
    os.makedirs(dirpath, exist_ok=True)
    
    # スクレイピングを開始する年月日を設定
    date = datetime.date(year, month, day)
    
    # 1月分スクレイピングする
    for day in range(1):
        for hour in [9, 21]:
        
            # 年月日を取得
            year = date.year
            month = date.month
            day = date.day
            
            # 高層の気象データスクレイピングクラスを作成する
            highriseWeather = HighriseWeatherDataScraping(year, month, day, hour, point)
            
            # ファイル名を設定
            filename = '{0:s}/{1:d}_{2:04d}_{3:02d}_{4:02d}_H{5:02d}.csv'.format(
                dirpath, point, year, month, day, hour)
            
            # スクレイピングを実行する。
            highriseWeather.scrape_high_rise_weather_data().write_to_csv(filename)
            
            # 1秒ディレイ
            time.sleep(1)
            
            
        # 日付を更新する
        date = date + datetime.timedelta(days=1)
        
##################################################
# 地上の気象データをスクレイピングする
##################################################
def scrape_ground_weather_data():
    
    # 都道府県、観測所、年月日
    prec_no = 40        # 茨城県
    block_no = 47629    # 水戸
    year = 2017
    month = 1
    day = 1
    
    # 地点ごとにディレクトリ作成
    dirpath = "{0:02d}_{1:05d}".format(prec_no, block_no)
    os.makedirs(dirpath, exist_ok=True)
    
    # スクレイピングを開始する年月日を設定
    date = datetime.date(year, month, day)
    
    # 1月分スクレイピングする
    for day in range(1):
        
        # 年月日を取得
        year = date.year
        month = date.month
        day = date.day
            
        # 地上の気象データスクレイピングクラスを作成する
        groundWeather = GroundWeatherDataScraping(prec_no, block_no, year, month, day)
            
        # ファイル名を設定
        filename = '{0:s}/{1:02d}-{2:02d}_{3:04d}_{4:02d}_{5:02d}.csv'.format(
            dirpath, prec_no, block_no, year, month, day)
            
        # スクレイピングを実行する。
        #groundWeather.scrape_weather_data()
        groundWeather.scrape().write_to_csv(filename)
            
        # 1秒ディレイ
        time.sleep(1)
        
        # 日付を更新する
        date = date + datetime.timedelta(days=1)
        

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    # 高層の気象データをスクレイピングする
    scrape_high_rise_weather_data()
    
    # 地上の気象データをスクレイピングする
    scrape_ground_weather_data()