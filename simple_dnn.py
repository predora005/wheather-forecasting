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
##################################################
if __name__ == '__main__':
	
	# コマンドライン引数のチェック
	argvs = sys.argv
	argc = len(argvs)
	if argc < 2:
		exe_name=argvs[0]
		print('Usage: python3 %s [input_csv_path]' % exe_name)
		quit()
	
	# CSVファイル読み込み
	input_csv_path = argvs[1]
	input_csv_data = []
	with open(input_csv_path, 'r', encoding='shift_jis') as f:
		reader = csv.reader(f)
		for row in reader:
			input_csv_data.append(row)
	
	# 入力データ取得：気温,降水量,風速
	temperature = get_temperature(input_csv_data)
	rainfall = get_rainfall(input_csv_data)
	wind_speed, wind_dir = get_wind_speed(input_csv_data)
	
	# 入力データ結合
	#input_data = numpy.concatenate(
	#	[temperature, rainfall, wind_speed, wind_dir], 1)
	input_data = numpy.stack(
		[temperature, rainfall, wind_speed, wind_dir], 1)
	
	# 出力データ取得：天気
	label_data = get_weather(input_csv_data)
	
	print(input_data.shape)
	print(label_data.shape)
	
	# 入力データ・出力データにNaNが
	# 含まれている行を削る
	isnan_row_input = numpy.isnan(input_data).any(axis=1)
	isnan_row_label = numpy.isnan(label_data).any(axis=1)
	isnan_row = numpy.logical_or(isnan_row_input, isnan_row_label)
	input_data = input_data[~isnan_row,]
	label_data = label_data[~isnan_row,]
	#input_data = numpy.delete(input_data, isnan_row, axis=0)
	#label_data = numpy.delete(label_data, isnan_row, axis=0)
	
	print(input_data.shape)
	print(label_data.shape)
	
	#data_num = input_data.shape[0]
	#input_data_dim = input_data.shape[1]
	#label_dim = weather[1]
	#input_isnan = numpy.isnan(input_data)
	#label_isnan = numpy.isnan(weather)
	#for i in range(data_num):
	#	for j in range(inpu_data_dim):
	#		print(numpy.isnan(weather[i]))
	
	 
	
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
	for i in range(1000):
		model.fit(
			input_data, label_data, 
			epochs=10, batch_size=32, shuffle=True, verbose=1)
		#print(model.metrics_names['accuracy'])
	
	
	
	
