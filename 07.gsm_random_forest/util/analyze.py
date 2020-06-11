# coding: utf-8

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score

import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.font_manager._rebuild() #キャッシュの削除
plt.rcParams['font.family'] = 'IPAGothic' # インストールしたフォントを指定

##################################################
# 正解率を表示する
##################################################
def print_accuracy(test_y, pred_y, class_names):
    
    num_class = len(class_names)
    
    # 正解率を表示する
    acc = accuracy_score(test_y, pred_y)
    print('Accuracy:{0:.3f}'.format(acc))
    
    # クラスごとの正解率を表示する
    for i, class_name in enumerate(class_names):
        
        class_idx = np.where(test_y.values == i)[0]
        class_y = test_y.iloc[class_idx]
        pred_y_i = pred_y[class_idx]
        
        #class_name = class_names[i]
        print( '  ## {0:s}'.format(class_name) )
        
        # iの正解率と不正解率を表示する
        for j in range(num_class):
            
            comp_name = class_names[j]  # 比較するクラス
            num_i = class_y.size        # iクラスの正解データ数
            
            if i == j:
                # iクラスの正解率を表示する
                if num_i > 0:
                    #acc = accuracy_score(class_y, pred_y_i)
                    num_j = accuracy_score(class_y, pred_y_i, normalize=False)
                    acc = num_j / num_i
                else:
                    acc = 0
                    
                #print('    Accuracy({0:s}-{1:s}):{2:.3f}'.format(class_name, comp_name, acc))
                print('    Accuracy({0:s}-{1:s}):{2:.3f}  {3:d}/{4:d}'.format(
                    class_name, comp_name, acc, num_j, num_i))
                
            else:
                # iクラスをjクラスと誤答した割合を表示する
                
                # iクラスが正解だが、jと分類してしまったデータ
                fail_y_j = np.where(pred_y_i == j)[0]
                num_j = fail_y_j.size
                
                # 不正解率を表示する
                if num_i > 0:
                    rate_fail = num_j / num_i
                else:
                    rate_fail = 0
                
                print('    Failure ({0:s}-{1:s}):{2:.3f}  {3:d}/{4:d}'.format(
                    class_name, comp_name, rate_fail, num_j, num_i))
                
##################################################
# 特徴量の重要度を表示する
##################################################
def show_importance_of_feature(importances, feature_names, png_file=None, csv_file=None):
    
    feature_importances = pd.DataFrame(importances, index=feature_names, columns=['Importance'])
    feature_importances = feature_importances.sort_values(by='Importance', ascending=False)
    feature_importances.plot(kind='bar', figsize=(20,20))
    
    if png_file is not None:
        plt.savefig(png_file, bbox_inches='tight')
    
    if csv_file is not None:
        feature_importances.to_csv(csv_file)
    
    