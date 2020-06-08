# coding: utf-8

import os, subprocess
import datetime, time
import pygrib
import numpy as np
import pandas as pd

##################################################
# MSMファイル名を取得する
##################################################
def get_msm_pall_file_name(year, month, day, hh):
    # ファイル名を設定する
    #   ex) Z__C_RJTD_20170101000000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin
    filename = 'Z__C_RJTD_{0:04d}{1:02d}{2:02d}{3:02d}0000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin'.format(
        year, month, day, hh)
        
    return filename
    
##################################################
# GSM指定気圧面データのファイル名を取得する
##################################################
def get_gsm_pall_file_name(year, month, day, hh):
    # ファイル名を設定する
    #   ex) Z__C_RJTD_20170102000000_GSM_GPV_Rjp_L-pall_FD0000-0312_grib2.bin
    filename = 'Z__C_RJTD_{0:04d}{1:02d}{2:02d}{3:02d}0000_GSM_GPV_Rjp_L-pall_FD0000-0312_grib2.bin'.format(
        year, month, day, hh)
        
    return filename
    
##################################################
# GSM地表データのファイル名を取得する
##################################################
def get_gsm_surf_file_name(year, month, day, hh):
    # ファイル名を設定する
    #   ex) Z__C_RJTD_20170102000000_GSM_GPV_Rjp_L-pall_FD0000-0312_grib2.bin
    filename = 'Z__C_RJTD_{0:04d}{1:02d}{2:02d}{3:02d}0000_GSM_GPV_Rjp_Lsurf_FD0000-0312_grib2.bin'.format(
        year, month, day, hh)
        
    return filename
    
##################################################
# URLを取得する
##################################################
def get_url(year, month, day, filename):
    
    # ディレクトリ名を設定する
    date_dir = '{0:04d}/{1:02d}/{2:02d}'.format(year, month, day)
    
    # URLを設定する
    url = 'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/{0:s}/{1:s}'.format(
        date_dir, filename)
        
    return url
    
##################################################
# MSMの初期時刻を取得する
##################################################
def get_msm_initial_hours():
    return [9, 12, 16, 18, 21, 0, 3, 6]

##################################################
# GSMの初期時刻を取得する
##################################################
def get_gsm_initial_hours():
    return [12, 18, 0, 6]

##################################################
# GSMの過去データをダウンロードする
##################################################
def download_gsm_files(output_dir, start_year, start_month, start_day, days):
    
    # 格納先ディレクトリを用意する
    os.makedirs(output_dir, exist_ok=True)
    
    # 取得を開始する年月日を設定
    date = datetime.date(start_year, start_month, start_day)
    
    # 初期時刻(UTC)
    initial_hours = get_gsm_initial_hours()
    
    # 指定した日数分のデータをダウンロードする
    days = 1    # 取得するデータの日数
    for i in range(days):
        
        # 年月日を取得
        year = date.year
        month = date.month
        day = date.day
        
        for hh in initial_hours:
            
            # 日を跨いだらdayを1加算する
            if hh == 0:
                day = day + 1
            
            # ファイル名を取得する
            filenames = [
                get_gsm_pall_file_name(year, month, day, hh),
                get_gsm_surf_file_name(year, month, day, hh)
            ]
            
            for filename in filenames:
                
                # ファイルが存在しなければダウンロードする
                output_filepath = os.path.join(output_dir, filename)
                if not os.path.isfile(output_filepath):
                    
                    # URLを設定する
                    url = get_url(year, month, day, filename)
                    
                    # 指定したURLからダウンロードする
                    result = subprocess.run(['curl', '-O', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=output_dir)
                    print(url)
                    
                    # 1秒ディレイ
                    time.sleep(1)
                    
        # 日付を更新する
        date = date + datetime.timedelta(days=1)

##################################################
# GSMの指定気圧面データをGRIB2からCSVに変換する
##################################################
def gsm_pall_grib2_to_csv(input_dir, output_dir, start_year, start_month, start_day, days):
    
    # 格納先ディレクトリを用意する
    os.makedirs(output_dir, exist_ok=True)
    
    # 取得を開始する年月日を設定
    date = datetime.date(start_year, start_month, start_day)
    
    # 初期時刻(UTC)
    initial_hours = get_gsm_initial_hours()
    
    # 指定した日数分のデータを読み込みCSCファイルに出力する
    for i in range(days):
        
        # 年月日を取得
        year = date.year
        month = date.month
        day = date.day
        
        # 格納用のDataFrameを用意する
        hh_df = None
        
        # 初期時刻ごとに処理する
        for hh in initial_hours:
            
            # 日を跨いだらdayを1加算する
            if hh == 0:
                day = day + 1
            
            # ファイル名を取得する
            filename = get_gsm_pall_file_name(year, month, day, hh)
            filepath = os.path.join(input_dir, filename)
            
            # GRIB2ファイルを読み込む
            grbs = pygrib.open(filepath)
            
            # 列名リストとndarrayを準備する
            column_names = []
            values_array = np.empty(0)
            
            # 指定気圧面のデータを取り出す
            levels = [850, 700, 500]
            for level in levels:
                
                # 指定気圧面のデータを取り出す
                plane_data = grbs.select(level=level, forecastTime=0)
                
                # 指定気圧面のうち学習に用いるデータのみを取り出し、
                # values_arrayに追加する
                for data in plane_data:
                    
                    if data.parameterName == 'Relative humidity':
                        param_name = '相対湿度'
                    elif data.parameterName == 'Temperature':
                        param_name = '温度'
                    elif data.parameterName == 'Vertical velocity':
                        param_name = '上昇流'
                    else:
                        continue
                
                    # 指定した(緯度,経度)に含まれる格子点のデータを抽出する
                    #   和歌山〜福島 (34,135)〜(38,141)
                    #   静岡〜いわき (35,138)〜(37,141)
                    data, latitudes, longitudes = data.data(lat1=35, lat2=37, lon1=138, lon2=141)
                    #print(data.shape, latitudes.min(), latitudes.max(), longitudes.min(), longitudes.max())
                    
                    # 物理量, 緯度, 経度を一次元化する
                    values = data.reshape(-1,)
                    latitudes = latitudes.reshape(-1,)
                    longitudes = longitudes.reshape(-1,)
                    
                    # 列名を作成し、リストに追加する
                    for i in range(latitudes.shape[0]):
                        column_name = '{0:d}hPa_lat{1:.3f}_long{2:.3f}_{3:s}'.format(
                            level, latitudes[i], longitudes[i], param_name)
                        column_names.append(column_name)
                    
                    # 物理量をndrrayに追加する
                    values_array = np.append(values_array, values)
                    
            # 物理量と列名からDataFrameを作成する
            values_array = values_array.reshape(1,values_array.shape[0])
            df = pd.DataFrame(data=values_array, columns=column_names)
            
            # 時刻データを追加する(UTCから日本時間に変更する)
            hh = hh - 9
            if hh < 0: hh = hh + 24
            df['時'] = hh
            
            # 1時刻のDataFrameを、1日分のDataFrameに追加する
            if hh_df is None:
                hh_df = df
            else:
                hh_df = hh_df.append(df, ignore_index=True)
        
        # 日付のデータを追加する
        hh_df['日付'] = date
        
        # 出力ファイル名
        filename = 'GSM_pall_{0:04d}_{1:02d}_{2:02d}.csv'.format(date.year, date.month, date.day)
        filepath = os.path.join(output_dir, filename)
        
        # 1日分のデータをCSVファイルに出力する
        hh_df = move_datetime_column_to_top(hh_df)
        hh_df.to_csv(filepath)
        
        # 日付を更新する
        date = date + datetime.timedelta(days=1)
        
##################################################
# 日付・時刻の列を先頭に移動する
##################################################
def move_datetime_column_to_top(df):
    """ 日付・時刻の列を先頭に移動する

    Args:
        df(DataFrame) : 変換対象のDataFrame

    Returns:
        DataFrame : 変換後のDataFrame
    """
    new_columns = ['日付', '時']
    for col in df.columns:
        if (col != '日付') and (col != '時'):
            new_columns.append(col)
    
    new_df = df.loc[:, new_columns]
    
    return new_df
    
##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    #
    # 1日単位でGSMのデータをCSVに出力する
    #
    
    # GSMデータの格納ディレクトリ
    cwd = os.getcwd()
    input_dir = os.path.join(cwd, 'input3')
    
    # 取得開始日付、取得する日数を設定する
    year = 2017
    month = 1
    day = 1
    days = 1
    
    # GSMの過去データをダウンロードする
    download_gsm_files(input_dir, year, month, day, days)
    
    # CSVファイルの出力先ディレクトリ
    cwd = os.getcwd()
    output_dir = os.path.join(cwd, 'input4')
    
    # GSMのデータをGRIB2からCSVに変換する
    gsm_pall_grib2_to_csv(input_dir, output_dir, year, month, day, days)
    