# -*- coding: utf-8 -*-
  
import sys, os
from common.format import *
import csv
import numpy
import pandas
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation

##################################################
# メイン
# [Args
#   train_csv_path : 訓練用データのCSVパス
#   test_csv_path  : テスト用データのCSVファイルパス
##################################################
if __name__ == '__main__':
	
	# コマンドライン引数のチェック
	argvs = sys.argv
	argc = len(argvs)
	if argc < 2:
		exe_name=argvs[0]
		print('Usage: python3 %s [train_csv_path] [test_csv_path]' % exe_name)
		quit()
	
	# CSVファイル読み込み
	#train_csv_path = argvs[1]
	#test_csv_path  = argvs[2]
	input_csv_path  = argvs[1]
	input_csv_data = []
	with open(input_csv_path, 'r', encoding='shift_jis') as f:
		reader = csv.reader(f)
		for row in reader:
			input_csv_data.append(row)
	
	# 入力データ取得：気温,降水量,風速
	temperature = get_temperature(input_csv_data)
	rainfall = get_rainfall(input_csv_data)
	wind_speed, wind_dir = get_wind_speed(input_csv_data)
	humidity = get_humidity(input_csv_data)
	daylight = get_daylight(input_csv_data)
	
	# 入力データ結合
	input_data = numpy.stack(
		[temperature, rainfall, wind_speed, wind_dir, humidity, daylight], 
		1)
	
	# 出力データ取得：天気
	label_data = get_weather(input_csv_data)
	
	# 入力データ・出力データにNaNが
	# 含まれている行を削る
	isnan_row_input = numpy.isnan(input_data).any(axis=1)
	isnan_row_label = numpy.isnan(label_data).any(axis=1)
	isnan_row = numpy.logical_or(isnan_row_input, isnan_row_label)
	input_data = input_data[~isnan_row,]
	label_data = label_data[~isnan_row,]
	
	# モデルの作成
	input_data_dim = input_data.shape[1]
	label_num = label_data.shape[1]
	model = Sequential()
	model.add(Dense(16, input_dim=input_data_dim))
	model.add(Activation('relu'))
	model.add(Dense(32))
	model.add(Activation('relu'))
	model.add(Dense(label_num))
	model.add(Activation('softmax'))
	#model.add(Dense(16, activation='relu', input_dim=input_data_dim))
	#model.add(Dense(32, activation='relu'))
	#model.add(Dense(class_num, activation='softmax'))
	
	model.summary()
	model.compile(
		optimizer='rmsprop',
		loss='binary_crossentropy',
		metrics=['accuracy'])
	
	# 学習実行
	for i in range(100):
		model.fit(
			input_data, label_data, 
			epochs=100, batch_size=32, shuffle=True, verbose=1)
		#print(model.metrics_names['accuracy'])
	
	
	
	
