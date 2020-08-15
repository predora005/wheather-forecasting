# coding: utf-8

import os
import subprocess
import pygrib

# 2020/08/01 15:00(UTC 06:00)の地上データをダウンロードする
cwd = os.getcwd()
url_surf = 'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/2020/08/01/Z__C_RJTD_20200801060000_GSM_GPV_Rjp_Lsurf_FD0000-0312_grib2.bin'
subprocess.run(['curl', '-O', url_surf], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cwd)

# GRIB2ファイルを読み込む
file_surf = os.path.join(cwd, os.path.basename(url_surf))
grbs = pygrib.open(file_surf)

# GRIB2ファイルの中身を表示する
for grb in grbs:
    print(grb)
    print(grb.parameterName, grb.name, grb.shortName)

# 指定した観測データを取り出す
prmsl = grbs.select(parameterName='Pressure reduced to MSL')
sp    = grbs.select(parameterName='Pressure')
uwind = grbs.select(parameterName='u-component of wind')
vwind = grbs.select(parameterName='v-component of wind')
temp  = grbs.select(parameterName='Temperature')
rh    = grbs.select(parameterName='Relative humidity')
lcc   = grbs.select(parameterName='Low cloud cover')
mcc   = grbs.select(parameterName='Medium cloud cover')
hcc   = grbs.select(parameterName='High cloud cover')
tcc   = grbs.select(parameterName='Total cloud cover')
tp    = grbs.select(parameterName='Total precipitation')
dswrf = grbs.select(parameterName='Downward short-wave radiation flux')

# 初期時刻から12時間後のデータを取り出す
fc12 = grbs.select(forecastTime=12)
print(fc12)

# 観測値を取得する
prmsl_fc0 = grbs.select(parameterName='Pressure reduced to MSL', forecastTime=0)[0]
values, lats, lons = prmsl_fc0.data()
print(values)

# 北緯34度から36度、東経135度から140度のデータを取り出す
prmsl_fc0 = grbs.select(parameterName='Pressure reduced to MSL', forecastTime=0)[0]
data, lats, lons = prmsl_fc0.data(lat1=34, lat2=36, lon1=135, lon2=140)
print(data)
print(lats)
print(lons)

# GRIB2ファイルを閉じる
grbs.close()


# 2020/08/01 15:00(UTC 06:00)の気圧面データをダウンロードする
cwd = os.getcwd()
url_pall = 'http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/2020/08/01/Z__C_RJTD_20200801060000_GSM_GPV_Rjp_L-pall_FD0000-0312_grib2.bin'
subprocess.run(['curl', '-O', url_pall], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=cwd)

# GRIB2ファイルを読み込む
file_pall = os.path.join(cwd, os.path.basename(url_pall))
grbs = pygrib.open(file_pall)

# GRIB2ファイルの中身を表示する
count = 0
for grb in grbs:
    print(grb)
    print(grb.parameterName, grb.name, grb.shortName)
    count += 1
    if count > 10:
        break
    
# 指定した観測データを取り出す
gh    = grbs.select(parameterName='Geopotential height')
uwind = grbs.select(parameterName='u-component of wind')
vwind = grbs.select(parameterName='v-component of wind')
temp  = grbs.select(parameterName='Temperature')
vv    = grbs.select(parameterName='Vertical velocity (pressure)')
rh    = grbs.select(parameterName='Relative humidity')

# 指定した気圧面のデータを取り出す
data_850hPa = grbs.select(level=850)
data_700hPa = grbs.select(level=700)
data_500hPa = grbs.select(level=500)
print(data_500hPa)

# 緯度,経度を取得する。
rh_500hPa = grbs.select(parameterName='Relative humidity', level=500, forecastTime=0)[0]
lats, lons = rh_500hPa.latlons()
print(lats)
print(lons)

# GRIB2ファイルを閉じる
grbs.close()
