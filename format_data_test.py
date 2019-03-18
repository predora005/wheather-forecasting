# -*- coding: utf-8 -*-
  
import sys, os
#sys.path.append(os.getcwd())
from common.format import *
import csv
import numpy
import pandas

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
	input_data = []
	with open(input_csv_path, 'r', encoding='shift_jis') as f:
		reader = csv.reader(f)
		for row in reader:
			input_data.append(row)
	#print(input_data)
	
	#input_df = pandas.read_csv(input_csv_path, encoding='shift_jis', header=1)
	#input_df = pandas.read_csv(input_csv_path, encoding='shift_jis', header=None)
	#print(input_df.shape)
	#print(input_df.head())
	
	# 気温取得
	temperature_df = get_temperature(input_data)
