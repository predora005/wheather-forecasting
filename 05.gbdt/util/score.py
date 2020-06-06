# coding: utf-8

import numpy as np
from sklearn.metrics import accuracy_score

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
                    acc = accuracy_score(class_y, pred_y_i)
                else:
                    acc = 0
                    
                print('    Accuracy({0:s}-{1:s}):{2:.3f}'.format(class_name, comp_name, acc))
                
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
                
                