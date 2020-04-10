# coding: utf-8

import os
import wcsv
import wdfproc
#from wcsv import *
#from wdfproc import *

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    cwd = os.getcwd()
    
    file_paths = wcsv.get_file_paths(cwd + '/Mito_40_47629')
    
    df = wcsv.read_ground(file_paths[0])
    print(df.head())
    
    columns = [ ('時','時'), ('湿度(％)','湿度(％)'), ('天気','天気') ]
    df1 = wdfproc.extract_from_columns(df, columns)
    print(df1.head())
    
    