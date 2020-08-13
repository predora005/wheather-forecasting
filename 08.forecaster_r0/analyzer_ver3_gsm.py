# coding: utf-8

import os

from analyzer import GsmDataAnalyzer2020Ver3

##################################################
# メイン
##################################################
if __name__ == '__main__':
    
    
    # GSMデータの分析クラス
    run_name = 'analysis_gsm_ver3'
    analyzer_param = {
        'base_dir'              : os.getcwd(),
        'temp_dir'              : 'temp',
        'input_dir'             : 'input8',
        'input2_dir'            : 'input2',
        'output_dir'            :  'output',
        'gsm_thinout_interval'  : (1,1),
        'weather_convert_mode'  : 'default',
        'class_names'           : ['Sunny', 'Cloud', 'Rain'],
        #'weather_convert_mode'  : 'rain_or_not',
        #'class_names'           : ['Except for Rain', 'Rain'],
        'label_name'            : 'Mito_天気'
    }
    analyzer = GsmDataAnalyzer2020Ver3(run_name, analyzer_param)
    
    # 分析実行
    analyzer.run()
