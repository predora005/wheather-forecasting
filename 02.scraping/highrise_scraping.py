# coding: utf-8

from scraping import HighriseWeatherDataScraping

import sys, os
import datetime, time
import re

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    # コマンドライン引数のチェック
    argvs = sys.argv
    argc = len(argvs)
    if argc < 5:
        exe_name=argvs[0]
        print('Usage: python3 %s [name] [point_no] [date] [days]' % exe_name)
        quit()
    
    # コマンドライン引数取り出し
    name = argvs[1]
    point_no  = int(argvs[2])
    date = argvs[3]
    days = int(argvs[4])
    
    # 日付を年・月・日に分解
    result = re.search(r"([0-9]+)-([0-9]+)-([0-9]+)", date)
    if result:
        year = int(result.group(1))
        month = int(result.group(2))
        day = int(result.group(3))
    else:
        print('"%s"Invalid date format !!' % (date))
        quit()
    
    # 地点ごとにディレクトリ作成
    homedir = os.path.expanduser('~')
    dirpath = '{0:s}/highrise_weather//{1:s}_{2:d}'.format(homedir, name, point_no)
    os.makedirs(dirpath, exist_ok=True)
    
    # スクレイピングを開始する年月日を設定
    date = datetime.date(year, month, day)
    
    # 高層気象データのスクレイピングを実行する
    for day in range(days):
        for hour in [9, 21]:
        
            # 年月日を取得
            year = date.year
            month = date.month
            day = date.day
            
            # ファイル名を設定
            #   ex) ~/Tateno_47646/Tateno_47646_2017_01_01_H09.csv
            filename = '{0:s}/{1:s}_{2:d}_{3:04d}_{4:02d}_{5:02d}_H{6:02d}.csv'.format(
                dirpath, name, point_no, year, month, day, hour)
            
            # ファイルが存在しない場合に限り、スクレイピングを実行する
            if not os.path.isfile(filename):
                
                # 高層の気象データスクレイピングクラスを作成する
                highriseWeather = HighriseWeatherDataScraping(year, month, day, hour, point_no)
                
                # スクレイピングを実行する。
                highriseWeather.scrape().write_to_csv(filename)
                
                # 1秒ディレイ
                time.sleep(1)

        # 日付を更新する
        date = date + datetime.timedelta(days=1)