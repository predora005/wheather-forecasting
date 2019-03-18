# -*- coding: utf-8 -*-
  
import numpy, pandas

##################################################
# 入力データ(input_data)から気温を抽出し整形して返す
##################################################
def get_temperature(input_data):
	
	col_num = len(input_data[3])
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
	data_num = len(input_data) - 6
	temperature_array = numpy.zeros(data_num, dtype=float)
	for i in range(data_num):
		index = i + 6
		value = float(input_data[index][value_col])
		quality = int(input_data[index][quality_col])
		if quality >= 5:
			temperature_array[i] = value
		else:
			temperature_array[i] = np.nan
		
	#print(temperature_array)
	
	# ndarrayをDataFrameに変換
	df = pandas.DataFrame(temperature_array, columns=['Temp.'])
	print(df)
	
	return df
	


