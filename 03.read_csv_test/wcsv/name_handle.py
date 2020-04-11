# coding: utf-8

import re

##################################################
# ファイル名から要素を取得する
##################################################
def elements_from_filename(filename):
    """ ファイル名から要素を取得する

    Args:
        filename(string) : ファイル名

    Returns:
        list[string] : 要素のリスト
    """
    result = re.search(r"(\D+)_(\d+)_(\d+)_(\d+)_(\d+)_(\d+).csv", filename)
    values = result.groups()
    elements = {
        'name'      : values[0], 
        'prec_no'   : int(values[1]),
        'block_no'  : int(values[2]),
        'year'      : int(values[3]),
        'month'     : int(values[4]),
        'day'       : int(values[5]),
    }

    return elements
    
##################################################
# ディレクトリ名から要素を取得する
##################################################
def elements_from_dirname(dirname):
    """ ディレクトリ名から要素を取得する

    Args:
        filename(string) : ファイル名

    Returns:
        dict : 要素のディクショナリ
    """
    result = re.search(r"(\D+)_(\d+)_(\d+)", dirname)
    values = result.groups()
    
    elements = {
        'place_name':values[0], 
        'prec_no': int(values[1]),
        'block_no': int(values[2])
    }
    
    return elements
    
