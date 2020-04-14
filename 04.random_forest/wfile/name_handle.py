# coding: utf-8

import re

##################################################
# ファイル名から要素を取得する(地上気象データ用)
##################################################
def elements_from_filename_ground(filename):
    """ ファイル名から要素を取得する(地上気象データ用)

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
# ディレクトリ名から要素を取得する(地上気象データ用)
##################################################
def elements_from_dirname_ground(dirname):
    """ ディレクトリ名から要素を取得する(地上気象データ用)

    Args:
        filename(string) : ファイル名

    Returns:
        dict : 要素のディクショナリ
    """
    result = re.search(r"(\D+)_(\d+)_(\d+)", dirname)
    values = result.groups()
    
    elements = {
        'name'      : values[0], 
        'prec_no'   : int(values[1]),
        'block_no'  : int(values[2])
    }
    
    return elements
    
##################################################
# ファイル名から要素を取得する(高層気象データ用)
##################################################
def elements_from_filename_highrise(filename):
    """ ファイル名から要素を取得する(高層気象データ用)

    Args:
        filename(string) : ファイル名

    Returns:
        list[string] : 要素のリスト
    """
    result = re.search(r"(\D+)_(\d+)_(\d+)_(\d+)_(\d+)_H(\d+).csv", filename)
    values = result.groups()
    elements = {
        'name'      : values[0], 
        'place_no'  : int(values[1]),
        'year'      : int(values[2]),
        'month'     : int(values[3]),
        'day'       : int(values[4]),
        'hour'      : int(values[5])
    }

    return elements
    
##################################################
# ディレクトリ名から要素を取得する(高層気象データ用)
##################################################
def elements_from_dirname_highrise(dirname):
    """ ディレクトリ名から要素を取得する(高層気象データ用)

    Args:
        filename(string) : ファイル名

    Returns:
        dict : 要素のディクショナリ
    """
    result = re.search(r"(\D+)_(\d+)", dirname)
    values = result.groups()
    
    elements = {
        'name'      : values[0], 
        'place_no'  : int(values[1]),
    }
    
    return elements
    
