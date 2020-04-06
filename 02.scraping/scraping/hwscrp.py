# coding: utf-8

import numpy as np
import pandas as pd

import requests
from bs4 import BeautifulSoup

##################################################
# 高層の気象データをスクレイピングするクラス。
##################################################
class HighriseWeatherDataScraping:
    """高層の気象データをスクレイピングするクラス。
    
    Attributes:
        __year (int)   : 年
        __month (int)  : 月
        __day (int)    : 日
        __hour (int)   : 時
        __point (int)  : 地点番号
        __df(DataFrame): スクレイピングで取得したデータ
    """

    ##############################
    # コンストラクタ
    ##############################
    def __init__(self, year, month, day, hour, point):
        """コンストラクタ
        
        Args:
            year (int): 年
            month (int): 月
            day  (int): 日
            hour (int): 時
            point  (int): 地点番号
            
        Returns:
           HighriseWeatherdataScraping: 自分自身
        """
        
        self.__year = year
        self.__month = month
        self.__day = day
        self.__hour = hour
        self.__point = point
        
    ##############################
    # URLを取得する
    ##############################
    def __get_url(self, year, month, day, hour, point):
        """ URLを取得する。
        
        Args:
            year (int): 年
            month (int): 月
            day  (int): 日
            hour (int): 時
            point  (int): 地点番号
            
        Returns:
            string: URL
        """
        
        url_first_half = "https://www.data.jma.go.jp/obd/stats/etrn/upper/view/hourly_usp.php?"
        url_second_half = "year={0:04d}&month={1:02d}&day={2:02d}&hour={3:d}&atm=&point={4:d}".format(year, month, day, hour, point)
        url = url_first_half + url_second_half
        
        return url
        
    ##############################
    # 気象データをスクレイピングする
    ##############################
    def __scrape_data(self, html, table_id):
        """気象データをスクレイピングする。
        
        Args:
            html (Response object): request.getで取得したResponseオブジェクト
            table_name (string): スクレイピング対象tableのid
            
        Return:
            DataFrame: スクレイピングしたデータ
        """
        
        # BeautifulSoupでHTMLを解析
        soup = BeautifulSoup(html.content, "html.parser")
        
        # id=table_idの<table>を抽出
        table = soup.find('table', id=table_id)
        
        # table内の全thを抽出
        th_all = table.find_all('th')
    
        # 列タイトルをリストに格納する
        table_column = []
        for th in th_all:
            table_column.append(th.string)
        
        # <table>内の全trを抽出。
        tr_all = table.find_all('tr')
        
        # 先頭のtrは抽出済みなので飛ばす
        tr_all = tr_all[1:]
        
        # 行と列の個数を算出し、ndarrayを作成
        number_of_cols = len(table_column)
        number_of_rows = len(tr_all)
        table_data = np.zeros((number_of_rows, number_of_cols), dtype=np.float32)
        
        # 各行のデータをndarrayに格納する
        for r, tr in enumerate(tr_all):
            td_all = tr.find_all('td')
            for c, td in enumerate(td_all):
                try:
                    table_data[r,c] = td.string
                except ValueError:
                    table_data[r,c] = np.nan

        # 抽出したデータのDataFrameを生成する
        df = pd.DataFrame(data=table_data, columns=table_column)
        
        return df
        
    ##############################
    # 地上の気象データをスクレイピングする
    ##############################
    def __scrape_ground_data(self, html):
        """地上の気象データをスクレイピングする。
        
        Args:
            html (Response object): request.getで取得したResponseオブジェクト
            
        Return:
            DataFrame: スクレイピングしたデータ
        """
        
        return self.__scrape_data(html, 'tablefix1')
        
    ##############################
    # 指定気圧面の気象データをスクレイピングする
    ##############################
    def __scrape_mandatory_level_data(self, html):
        """指定気圧面の気象データをスクレイピングする。
        
        Args:
            html (Response object): request.getで取得したResponseオブジェクト
            
        Return:
            DataFrame: スクレイピングしたデータ
        """
        
        return self.__scrape_data(html, 'tablefix2')
        
    ##############################
    # 高層の気象データをスクレイピングする
    ##############################
    def scrape_high_rise_weather_data(self):
        """高層の気象データをスクレイピングする。
        
        Returns:
            HighriseWeatherdataScraping: 自分自身
        """
        
        # 指定URLのHTMLデータを取得
        url = self.__get_url(self.__year, self.__month, self.__day, self.__hour, self.__point)
        html = requests.get(url)
        print(url)
        
        # BeautifulSoupでHTMLを解析
        df1 = self.__scrape_ground_data(html)
        df2 = self.__scrape_mandatory_level_data(html)
        
        # 地上の気象データと指定気圧面の気象データをひとつのDataFrameに結合する
        df2.columns = df1.columns.values
        self.__df = pd.concat([df1, df2], ignore_index=True)
        
        return self
        
    ##############################
    # CSVファイルに出力する
    ##############################
    def write_to_csv(self, filepath):
        """CSVファイルに出力する
        
        Args:
            html (Response object): request.getで取得したResponseオブジェクト
        """
        
        self.__df.to_csv(filepath)