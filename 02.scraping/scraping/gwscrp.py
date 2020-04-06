# coding: utf-8

import numpy as np
import pandas as pd

import requests
from bs4 import BeautifulSoup

from itertools import product

##################################################
# 地上の気象データをスクレイピングするクラス。
##################################################
class GroundWeatherDataScraping:
    """ 地上の気象データをスクレイピングするクラス。
    
    Attributes:
        __prec_no(int) : 都道府県番号
        __block_no(int): 観測所番号
        __year (int)   : 年
        __month (int)  : 月
        __day (int)    : 日
        __df(DataFrame): スクレイピングで取得したデータ
    """

    ##############################
    # コンストラクタ
    ##############################
    def __init__(self, prec_no, block_no, year, month, day):
        """ コンストラクタ
        
        Args:
            prec_no     (int) : 都道府県番号
            block_no    (int) : 観測所番号
            year        (int) : 年
            month       (int) : 月
            day         (int) : 日
            
        Returns:
           GroundWeatherdataScraping: 自分自身
        """
        
        self.__prec_no = prec_no
        self.__block_no = block_no
        self.__year = year
        self.__month = month
        self.__day = day
        
    ##############################
    # URLを取得する
    ##############################
    def __get_url(self, prec_no, block_no, year, month, day):
        """ URLを取得する。
        
        Args:
            prec_no     (int) : 都道府県番号
            block_no    (int) : 観測所番号
            year        (int) : 年
            month       (int) : 月
            day         (int) : 日
        
        Returns:
            string: URL
        """
        
        # https://www.data.jma.go.jp/obd/stats/etrn/view/hourly_s1.php?prec_no=40&block_no=47629&year=2017&month=1&day=1&view=
        url_first_half = "https://www.data.jma.go.jp/obd/stats/etrn/view/hourly_s1.php?"
        url_second_half = "prec_no={0:d}&block_no={1:d}&year={2:d}&month={3:d}&day={4:d}".format(prec_no, block_no, year, month, day)
        url = url_first_half + url_second_half
        
        return url
        
    ##############################
    # テーブル見出しの行数を取得する。
    ##############################
    def __get_heading_row_num(self, table):
        """ テーブル見出しの行数を取得する。
        
        Args:
            table (bs4.element.Tag) : 対象のテーブル
        Return:
            int : テーブル見出しの行数
        """
        
        # table内の全trを抽出
        tr_all = table.find_all('tr')
        
        # テーブル見出しの行数をカウントする
        heading_row_num = 0
        for tr in tr_all:
            
            # <th>要素を持つ行があれば行数をカウントアップする
            th = tr.find('th')
            if th is not None:
                heading_row_num = heading_row_num + 1
        
        return heading_row_num
        
    ##############################
    # テーブル見出しの列数を取得する。
    ##############################
    def __get_heading_col_num(self, table):
        """ テーブル見出しの列数を取得する。
        
        Args:
            table (bs4.element.Tag) : 対象のテーブル
        Return:
            int : テーブル見出しの列数
        """
        
        # table内の全trを抽出
        tr_all = table.find_all('tr')
        
        # テーブル見出しの列数を取得する
        heading_col_num = 0
        for tr in tr_all:
            
            # <th>を持つ行(<tr>)があれば列数をカウントする
            th_all = tr.find_all('th')
            if th_all:
                col_num = 0
                for th in th_all:
                    col_num += int(th.get('colspan', 1))
                    
                # 列数の最大値を更新する
                heading_col_num = max(heading_col_num, col_num)
        
        return heading_col_num
        
    ##############################
    # テーブル見出しを取得する。
    ##############################
    def __get_heading(self, table, col_num):
        """ テーブル見出しの列数を取得する。
        
        Args:
            table (bs4.element.Tag) : 対象のテーブル
            col_num (int)           : 見出しの列数
        Return:
            table_heading : テーブル見出しを格納したリスト
        """
        
        # table内の全trを抽出
        tr_all = table.find_all('tr')
        
        # テーブル見出し用のリストを用意する
        table_heading = []

        # テーブル見出しをリストに格納する
        #   - num_reapeat[列数] : rowspanが2以上のとき行方向に繰り返しセットする回数
        #   - col_th[列数] : rowspanが2以上のとき行方向に繰り返しセットする<th>要素
        num_repeat = [ 0 for col in range(col_num) ]
        col_th = [ None for col in range(col_num) ]
        for tr in tr_all:
            
            # <th>要素を持つ行に対して処理を行う
            th_all = tr.find_all('th')
            if th_all:
                
                # 全<th>要素をpop()で取出し続ける
                cols = []
                col = 0
                while col < col_num:
                    # 前の行でrowspanがある場合は、前回記憶した<th>要素を取り出す
                    if num_repeat[col] > 0:
                        th = col_th[col]
                        num_repeat[col] -= 1
                    else:
                        th = th_all.pop(0)
                        rowspan = int(th.get('rowspan', 1))
                        if rowspan > 1:
                            # rowspanが2以上のとき、
                            # 次の行以降の繰り返し回数と、<th>要素を記録する
                            num_repeat[col] = rowspan - 1
                            col_th[col] = th
                    
                    # colspan回数分、<th>の中身をリストに追加する
                    colspan = int(th.get('colspan', 1))
                    for c in range(colspan):
                        cols.append(th.get_text(strip=True))
                        col += 1
                
                # 当該行の列要素をリストに追加する
                table_heading.append(cols)
        
        return table_heading
        
    ##############################
    # 気象データをスクレイピングする。
    ##############################
    def __scrape_data(self, html):
        """ 気象データをスクレイピングする。
        
        Args:
            html (Response object): request.getで取得したResponseオブジェクト
        Return:
            DataFrame: スクレイピングしたデータ
        """
        
        # BeautifulSoupでHTMLを解析
        soup = BeautifulSoup(html.content, "html.parser")
        
        # id=table_idの<table>を抽出
        table = soup.find('table', id="tablefix1")

        # テーブル見出しの行数をカウントする
        #heading_row_num = self.__get_heading_row_num(table)

        # テーブル見出しの列数を取得する
        heading_col_num = self.__get_heading_col_num(table)

        # テーブル見出しのリストを取得する
        table_heading = self.__get_heading(table, heading_col_num)
        
        # <table>内の全trを抽出。
        tr_all = table.find_all('tr')
        
        # ヘッダー行は抽出済みなので飛ばす
        heading_row_num = len(table_heading)
        tr_all = tr_all[heading_row_num:]
        
        # 行と列の個数を算出し、ndarrayを作成
        number_of_cols = heading_col_num
        number_of_rows = len(tr_all)
        
        table_data = [ [''] * number_of_cols for r in range(number_of_rows)]

        # 各行のデータをndarrayに格納する
        for r, tr in enumerate(tr_all):
            td_all = tr.find_all('td')
            for c, td in enumerate(td_all):
                img = td.find('img')
                if img is not None:
                    table_data[r][c] = img.get('alt')
                else:
                    table_data[r][c] = td.get_text()

        # 抽出したデータのDataFrameを生成する
        columns = pd.MultiIndex.from_arrays(table_heading)
        df = pd.DataFrame(data=table_data, columns=columns)
                
        return df
        
    ##############################
    # 気象データをスクレイピングする
    ##############################
    def scrape(self):
        """気象データをスクレイピングする。
        
        Returns:
            HighriseWeatherdataScraping: 自分自身
        """
        
        # 指定URLのHTMLデータを取得
        url = self.__get_url(self.__prec_no, self.__block_no, self.__year, self.__month, self.__day)
        html = requests.get(url)
        print(url)
        
        # BeautifulSoupでHTMLを解析
        self.__df = self.__scrape_data(html)
        
        return self
        
    ##############################
    # スクレイピング結果をCSVファイルに出力する
    ##############################
    def write_to_csv(self, filepath):
        """スクレイピング結果をCSVファイルに出力する。
        
        Args:
            filepath (string) : 出力先ファイルパス
        """
        
        self.__df.to_csv(filepath)