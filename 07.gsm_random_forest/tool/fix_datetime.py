# coding: utf-8

import os, datetime
import pandas as pd

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    # 変換前データの読み込み
    before_file = os.path.join( 'temp', 'gsm_intv_1x1.csv')
    before_df = pd.read_csv(before_file, index_col=0, parse_dates=[1])
    
    # 変換後CSVのディレクトリ
    after_surf = os.path.join( 'input6', 'surf')
    after_pall = os.path.join( 'input6', 'pall')
    
    # 変換後CSVのディレクトリ作成
    os.makedirs(after_surf, exist_ok=True)
    os.makedirs(after_pall, exist_ok=True)
    
    # 変換を開始する年月日・変換対象日数を設定
    date = datetime.date(2016, 1, 2)
    days = 366 + 365*3 - 1
    #days = 1
    
    # 最初の行のインデックスNo.を取得する(最初の1データは読み飛ばす)
    tmpdate = date - datetime.timedelta(days=1)
    before_date = '{0:04d}-{1:02d}-{2:02d}'.format(tmpdate.year, tmpdate.month, tmpdate.day)
    before_hh = 9
    first_row = before_df[(before_df['日付']==before_date) & (before_df['時']==before_hh)]
    index = first_row.index.values[0]

    # 指定した日数分のデータを読み込みCSVファイルに出力する
    first_row =True
    for i in range(days):
        
        # 年月日
        year1 = date.year
        month1 = date.month
        day1 = date.day
        
        # 修正対象の行を抽出する
        new_df = before_df.iloc[index:index+4,]
        new_df = new_df.copy()
        new_df = new_df.reset_index()

        # 修正後の日付
        date1 = '{0:04d}-{1:02d}-{2:02d}'.format(year1, month1, day1)
        
        # 修正後の時刻
        hh1 = 3
        hh2 = 9
        hh3 = 15
        hh4 = 21
        
        # 日付と時刻を修正する
        new_df.loc[0, '日付'] = date1
        new_df.loc[0, '時'] = hh1
        new_df.loc[1, '日付'] = date1
        new_df.loc[1, '時'] = hh2
        new_df.loc[2, '日付'] = date1
        new_df.loc[2, '時'] = hh3
        new_df.loc[3, '日付'] = date1
        new_df.loc[3, '時'] = hh4
        
        # 最初の行であれば列名を取得し、
        # 抽出・削除対象の列名リストを作成する
        if first_row:
            columns = new_df.columns
            surf_columns = [col for col in columns if 'Surf' in col]
            surf_columns.insert(0, '日付')
            surf_columns.insert(1, '時')
            pall_columns =  [col for col in columns if 'Surf' not in col]
            first_row = False
        
        # 地表データ(surf)、指定気圧面データ(pall)を抽出する
        surf_df = new_df[surf_columns]
        pall_df = new_df[pall_columns]
        
        # 変換後CSVのファイルパス作成
        surf_file = 'GSM_surf_{0:04d}_{1:02d}_{2:02d}.csv'.format(year1, month1, day1)
        pall_file = 'GSM_pall_{0:04d}_{1:02d}_{2:02d}.csv'.format(year1, month1, day1)
        surf_csv = os.path.join(after_surf, surf_file)
        pall_csv = os.path.join(after_pall, pall_file)
        
        # CSVに出力する
        surf_df.to_csv(surf_csv)
        pall_df.to_csv(pall_csv)
        
        # 日付を更新する
        date = date + datetime.timedelta(days=1)
        
        # インデックスを更新する
        index = index + 4

