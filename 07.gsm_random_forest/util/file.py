# coding: utf-8

import os

##################################################
# 指定したディレクトリから
# 指定した拡張子のファイルのリストを取得する
##################################################
def get_file_paths(dir_path, extension=None):
    """ 指定したディレクトリから
        指定した拡張子のファイルのリストを取得する
    
    Args:
        dir_path    (string)            : ディレクトリパス
        extension   (string, optional)  : 拡張子

    Returns:
        list[string] : ファイルパスのリスト
    """
    file_paths = []
    
    # sortedを使用してファイル名の昇順に読み込む
    for filename in sorted(os.listdir(dir_path)):
        
        file_path = os.path.join(dir_path,filename)
        
        # ディレクトリの場合はpass
        if os.path.isdir(file_path):
            continue
        
        # 拡張子が一致したらリストに追加
        if extension is None:
            # 拡張子の指定無しの場合は無条件に追加
            file_paths.append(file_path)
        else:
            base,ext = os.path.splitext(filename)
            if ext == extension:
                file_paths.append(file_path)
        
    return file_paths