# coding: utf-8

from scraping import GroundWeatherDataScraping

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
    if argc < 6:
        exe_name=argvs[0]
        print('Usage: python3 %s [name] [prec_no] [block_no] [date] [days]' % exe_name)
        quit()
    
    # コマンドライン引数取り出し
    name = argvs[1]
    prec_no  = int(argvs[2])
    block_no  = int(argvs[3])
    date = argvs[4]
    days = int(argvs[5])
    
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
    dirpath = '{0:s}/ground_weather/{1:s}_{2:02d}_{3:05d}'.format(homedir, name, prec_no, block_no)
    os.makedirs(dirpath, exist_ok=True)
    
    # スクレイピングを開始する年月日を設定
    date = datetime.date(year, month, day)
    
    # 地上気象データのスクレイピングを実行する
    for day in range(days):

        # 年月日を取得
        year = date.year
        month = date.month
        day = date.day
            
        # ファイル名を設定
        #   ex) ~/Tateno_47646/Tateno_47646_2017_01_01_H09.csv
        filename = '{0:s}/{1:s}_{2:02d}_{3:02d}_{4:04d}_{5:02d}_{6:02d}.csv'.format(
            dirpath, name, prec_no, block_no, year, month, day)

        # ファイルが存在しない場合に限り、スクレイピングを実行する
        if not os.path.isfile(filename):
            
            # 地上の気象データスクレイピングクラスを作成する
            groundWeather = GroundWeatherDataScraping(prec_no, block_no, year, month, day)
                
            # スクレイピングを実行する。
            groundWeather.scrape().write_to_csv(filename)
            
            # 1秒ディレイ
            time.sleep(1)

        # 日付を更新する
        date = date + datetime.timedelta(days=1)