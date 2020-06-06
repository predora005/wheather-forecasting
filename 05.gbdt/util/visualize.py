# coding: utf-8

import pydotplus
from sklearn.tree import export_graphviz, plot_tree

##################################################
# Graphvizのグラフをファイルに出力する
##################################################
def export_graphviz(file_name, estimators, feature_names, class_names):
    """ Graphvizのグラフをファイルに出力する

    Args:
        file_name(string)               : ファイル名
        feature_names(list of string)   : 特徴量の名称リスト
        class_names(list of string)     : クラス名のリスト
    """
    dot_data = export_graphviz(
        estimators, 
        feature_names=feature_names,
        class_names=class_names,  
        filled=True, 
        rounded=True)
    graph = pydotplus.graph_from_dot_data( dot_data )
    graph.write_png(file_name)
    
