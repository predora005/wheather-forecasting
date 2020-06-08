# coding: utf-8

import os
import subprocess
import pygrib

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    # 2017/01/01のデータをダウンロードする
    url = 'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/2017/01/01/Z__C_RJTD_20170101000000_MSM_GPV_Rjp_L-pall_FH00-15_grib2.bin'
    #url = 'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/2017/01/01/Z__C_RJTD_20170101000000_MSM_GPV_Rjp_Lsurf_FH00-15_grib2.bin'
    #url = 'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/2017/01/01/Z__C_RJTD_20170101000000_GSM_GPV_Rjp_Lsurf_FD0000-0312_grib2.bin'
    cwd = os.getcwd()
    input_dir = os.path.join(cwd, 'input3')
    result = subprocess.run(['curl', '-O', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=input_dir)
    #result = subprocess.run(['curl', '-O', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # 気象データファイルを読み込む
    basename = os.path.basename(url)
    file_path = os.path.join(input_dir, basename)
    grbs = pygrib.open(file_path)
    
    # 気象データを標準出力する
    for grb in grbs:
        print(grb)
    
    # 相対湿度を取り出す
    print('==================================================')
    grb = grbs.select(parameterName='Relative humidity')
    print(grb)
    
    # 975hPa気圧面の時刻0のデータを取り出す
    print('==================================================')
    grb = grbs.select(level=975, forecastTime=0)
    print(grb)
    
    # 相対湿度のキーを全て表示する
    print('==================================================')
    grb = grbs.select(parameterName='Relative humidity')[1]
    print(grb)
    for key in grb.keys():
        print(key)
        #print(key, grb[key])
        #if key in grb:
        #    print(key, grb[key])
        #else:
        #    print(key + " is not in grb.")

    # # 緯度, 経度を取り出す
    print('==================================================')
    grb = grbs.select(forecastTime=0)[0]
    lats, lons = grb.latlons()
    print('latitude:', lats)
    print('longitude:', lons)
    
    #for key in grb.keys():
    #    print(key, grb[key])
    #print('==============================')
    #grb = grbs.select(forecastTime=0)[0]
    #for key in grb.keys():
    #    print(key, grb[key])
    #print(grb)
    #print(grb.keys())
    #print('==============================')
    #grb = grbs.select(forecastTime=1)[0]
    #print(grb)
    #print('==============================')
    #grb = grbs.message(1)
    #print(grb)
    #print('==============================')
    #grb = grbs.message(2)
    #print(grb)
    #print('==============================')
    #grb = grbs.select(name='fcst time')
    #print(grb)
    
    
    