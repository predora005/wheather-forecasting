# -*- coding: utf-8 -*-

import math
import numpy, pandas

##################################################
# 定数
##################################################
ROW_DATA_START = 6

# 風向を角度(-PI~PI)に変換する
WIND_DIRECTION_MAP = {
  '北': 0,          '北北東': math.pi/8,    '北東': math.pi/4,    '東北東': math.pi*3/8,
  '東': math.pi/2,  '東南東': math.pi*5/8,  '南東': math.pi*3/4,  '南南東': math.pi*7/8, 
  '南': math.pi,    '南南西': -math.pi*7/8, '南西': -math.pi*3/4, '西南西': -math.pi*5/8,
  '西': -math.pi/2, '西北西': -math.pi*3/8, '北西': -math.pi/4,   '北北西': -math.pi/8
}

##################################################
# 入力データ(input_data)からデータの列数を取得する
##################################################
def get_col_num(input_data):
	
	col_num = len(input_data[3])
	return col_num
	
##################################################
# 入力データ(input_data)から気温を抽出し整形して返す
##################################################
def get_temperature(input_data):
	
	col_num = get_col_num(input_data)
	#print(col_num)
	
	# 気温のデータの中から、
	# 値そのものの列と、品質情報の列の列番号を取得する
	value_col = 0
	quality_col = 0
	
	for i in range(col_num):
		name = input_data[3][i]
		if name.find('気温') >= 0 :
			info = input_data[5][i]
			if not info:
				value_col = i
			elif info.find('品質情報') >= 0 :
				quality_col = i
	#print(value_col)
	#print(quality_col)
	
	# 品質情報が8(正常値),5(20%以下の欠損)なら正常値を設定し、
	# それ以外の場合はNaNを設定する
	# 最初の6行はヘッダーなので読み飛ばす
	# ndarray(temperature_array)に結果を格納する
	data_num = len(input_data) - ROW_DATA_START
	temperature_array = numpy.zeros(data_num, dtype=float)
	for i in range(data_num):
		index = i + ROW_DATA_START
		value = float(input_data[index][value_col])
		quality = int(input_data[index][quality_col])
		if quality >= 5:
			temperature_array[i] = value
		else:
			temperature_array[i] = np.nan
		
	#print(temperature_array)
	return temperature_array
	
	# ndarrayをDataFrameに変換
	#df = pandas.DataFrame(temperature_array, columns=['Temp.'])
	#print(df)
	
	#return df
	
##################################################
# 入力データ(input_data)から降水量を抽出し整形して返す
##################################################
def get_rainfall(input_data):
	
	col_num = get_col_num(input_data)
	
	# 降水量のデータの中から、
	# 値そのものの列と、品質情報の列の列番号を取得する
	value_col = 0
	quality_col = 0
	
	for i in range(col_num):
		name = input_data[3][i]
		if name.find('降水量') >= 0 :
			info = input_data[5][i]
			if not info:
				value_col = i
			elif info.find('品質情報') >= 0 :
				quality_col = i
	#print(value_col)
	#print(quality_col)
	
	# 品質情報が8(正常値),5(20%以下の欠損)なら正常値を設定し、
	# それ以外の場合はNaNを設定する
	# 最初の6行はヘッダーなので読み飛ばす
	# ndarray(rainfall_array)に結果を格納する
	data_num = len(input_data) - ROW_DATA_START
	rainfall_array = numpy.zeros(data_num, dtype=float)
	for i in range(data_num):
		index = i + ROW_DATA_START
		value = float(input_data[index][value_col])
		quality = int(input_data[index][quality_col])
		if quality >= 5:
			rainfall_array[i] = value
		else:
			rainfall_array[i] = np.nan
		
	#print(rainfall_array)
	return rainfall_array
	
	# ndarrayをDataFrameに変換
	#df = pandas.DataFrame(temperature_array, columns=['Temp.'])
	#print(df)
	
	#return df
	
##################################################
# 入力データ(input_data)から風速(速度と風向き)を
# 抽出し整形して返す
##################################################
def get_wind_speed(input_data):
	
	col_num = get_col_num(input_data)
	
	# 風速のデータの中から、
	# 風速(m/s), 風速(m/s)の品質, 風向, 風向の品質が
	# 格納されている列の列番号を取得する
	value_speed_col = 0
	quality_speed_col = 0
	value_dir_col = 0
	quality_dir_col = 0
	
	for i in range(col_num):
		name = input_data[3][i]
		if name.find('風速') >= 0 :
			info1 = input_data[4][i]
			info2 = input_data[5][i]
			
			####################
			# 風速(m/s)
			####################
			if not info1:
				if not info2:
					value_speed_col = i
				elif info2.find('品質情報') >= 0 :
					quality_speed_col = i
			
			####################
			# 風向
			####################
			else:
				if not info2:
					value_dir_col = i
				elif info2.find('品質情報') >= 0 :
					quality_dir_col = i
	
	# 品質情報が8(正常値),5(20%以下の欠損)なら正常値を設定し、
	# それ以外の場合はNaNを設定する
	# 最初の6行はヘッダーなので読み飛ばす
	# ndarray(rainfall_array)に結果を格納する
	data_num = len(input_data) - ROW_DATA_START
	wind_speed_array = numpy.zeros(data_num, dtype=float)
	wind_dir_array = numpy.zeros(data_num, dtype=float)
	for i in range(data_num):
		index = i + ROW_DATA_START
		
		# 風速(m/s)
		value = float(input_data[index][value_speed_col])
		quality = int(input_data[index][quality_speed_col])
		if quality >= 5:
			wind_speed_array[i] = value
		else:
			wind_speed_array[i] = np.nan
		
		# 風向
		value = input_data[index][value_dir_col]
		quality = int(input_data[index][quality_dir_col])
		if quality >= 5:
			# 静穏の場合は風速=0にする
			if value.find('静穏') >= 0 :
				wind_dir_array[i] = 0
			else:
				wind_dir_array[i] = WIND_DIRECTION_MAP[value]
		else:
			wind_dir_array[i] = np.nan
		
	#print(rainfall_array)
	return (wind_speed_array, wind_dir_array)
	
	# ndarrayをDataFrameに変換
	#df = pandas.DataFrame(temperature_array, columns=['Temp.'])
	#print(df)
	
	#return df
	






