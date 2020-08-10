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
        
        print( '  ## {0:s}'.format(class_name) )
        
        # iの正解率と不正解率を表示する
        for j in range(num_class):
            
            comp_name = class_names[j]  # 比較するクラス
            num_i = class_y.size        # iクラスの正解データ数
            
            if i == j:
                # iクラスの正解率を表示する
                if num_i > 0:
                    num_j = accuracy_score(class_y, pred_y_i, normalize=False)
                    acc = num_j / num_i
                else:
                    acc = 0
                    
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
# 適合率と再現率を表示する
##################################################
def print_precision_and_recall(test_y, pred_y, class_names):
    
    num_class = len(class_names)
    
    # クラスごとの適合率を表示する
    print('Precision:')
    for i, class_name in enumerate(class_names):
        
        class_idx = np.where(pred_y == i)[0]
        pred_y_i = pred_y[class_idx]        # クラスiの予測データ
        class_y = test_y.iloc[class_idx]    # クラスiの正解データ
        
        num_i = class_y.shape[0]            # iクラスと予測したデータ数

        # クラスiと予測したデータのうち、実際にクラスjが正解のデータの数
        true_i = np.where(class_y.values == i)[0]
        num_j = true_i.size
        
        # 適合率
        precision = float(num_j) / float(num_i)
        
        print('  ## {0:s}: {1:.3f}  {2:d}/{3:d}'.format(class_name, precision, num_j, num_i) )
    
    # クラスごとの再現率を表示する
    print('Recall:')
    for i, class_name in enumerate(class_names):
        
        class_idx = np.where(test_y.values == i)[0]
        pred_y_i = pred_y[class_idx]        # クラスiの予測データ
        class_y = test_y.iloc[class_idx]    # クラスiの正解データ
        
        num_i = class_y.shape[0]    # iクラスの正解データ数
        
        # クラスiが正解のデータのうち、クラスiと予測したデータの数
        pred_i = np.where(pred_y_i == i)[0]
        num_j = pred_i.size

        # 再現率
        recall = float(num_j) / float(num_i)
        
        print('  ## {0:s}: {1:.3f}  {2:d}/{3:d}'.format(class_name, recall, num_j, num_i) )
                
##################################################
# 正解率を表示する(One-Hotラベル用)
##################################################
def print_accuracy_one_hot(test_y, pred_y, class_names):
    
    num_class = len(class_names)
    
    # 正解率を表示する
    result = np.where(np.argmax(test_y, axis=1)==np.argmax(pred_y, axis=1), 1, 0)
    acc = np.mean(result)
    print('Accuracy:{0:.3f}'.format(acc))
    
    # クラスごとの正解率を表示する
    for i, class_name in enumerate(class_names):
        
        class_idx = np.where(np.argmax(test_y, axis=1)==i)
        class_y = test_y[class_idx]     # クラスiの正解データ
        pred_y_i = pred_y[class_idx]    # クラスiの予測データ
        
        print( '  ## {0:s}'.format(class_name) )
        
        # iの正解率と不正解率を表示する
        for j in range(num_class):
            
            comp_name = class_names[j]  # 比較するクラス
            num_i = class_y.shape[0]    # iクラスの正解データ数
            
            if i == j:
                # iクラスの正解率を表示する
                if num_i > 0:
                    result = np.where(np.argmax(class_y, axis=1)==np.argmax(pred_y_i, axis=1), 1, 0)
                    num_j = np.sum(result)
                    acc = np.mean(result)
                else:
                    acc = 0
                    
                print('    Accuracy({0:s}-{1:s}):{2:.3f}  {3:d}/{4:d}'.format(
                    class_name, comp_name, acc, num_j, num_i))
                
            else:
                # iクラスをjクラスと誤答した割合を表示する
                
                # iクラスが正解だが、jと分類してしまったデータ
                result = np.where(np.argmax(pred_y_i, axis=1) == j, 1, 0)
                num_j = np.sum(result)

                # 不正解率を表示する
                if num_i > 0:
                    rate_fail = num_j / num_i
                else:
                    rate_fail = 0
                
                print('    Failure ({0:s}-{1:s}):{2:.3f}  {3:d}/{4:d}'.format(
                    class_name, comp_name, rate_fail, num_j, num_i))

##################################################
# 適合率と再現率を表示する(One-Hotラベル用)
##################################################
def print_precision_and_recall_one_hot(test_y, pred_y, class_names):
    
    num_class = len(class_names)
    
    # クラスごとの適合率を表示する
    print('Precision:')
    for i, class_name in enumerate(class_names):
        
        class_idx = np.where(np.argmax(pred_y, axis=1)==i)
        pred_y_i = pred_y[class_idx]    # クラスiの予測データ
        class_y = test_y[class_idx]     # クラスiの正解データ
        
        num_i = pred_y_i.shape[0]    # iクラスと予測したデータ数
        
        # クラスiと予測したデータのうち、実際にクラスjが正解のデータの数
        result = np.where(np.argmax(class_y, axis=1)==np.argmax(pred_y_i, axis=1), 1, 0)
        num_j = np.sum(result)
        
        # 適合率
        precision = np.mean(result)
        
        print('  ## {0:s}: {1:.3f}  {2:d}/{3:d}'.format(class_name, precision, num_j, num_i) )
        
    # クラスごとの再現率を表示する
    print('Recall:')
    for i, class_name in enumerate(class_names):
        
        class_idx = np.where(np.argmax(test_y, axis=1)==i)
        class_y = test_y[class_idx]     # クラスiの正解データ
        pred_y_i = pred_y[class_idx]    # クラスiの予測データ
        
        num_i = class_y.shape[0]    # iクラスの正解データ数
        
        # クラスiが正解のデータのうち、クラスiと予測したデータの数
        result = np.where(np.argmax(class_y, axis=1)==np.argmax(pred_y_i, axis=1), 1, 0)
        num_j = np.sum(result)
        
        # 再現率
        recall = np.mean(result)
        
        print('  ## {0:s}: {1:.3f}  {2:d}/{3:d}'.format(class_name, recall, num_j, num_i) )
        

##################################################
# 特徴量の重要度を出力する(scikit-learnの決定木用)
##################################################
def output_importance_of_feature_for_sklearn_dtree(importances, feature_names, png_path=None, csv_path=None):
    
    feature_importances = pd.DataFrame(importances, index=feature_names, columns=['Importance'])
    feature_importances = feature_importances.sort_values(by='Importance', ascending=False)
    
    if csv_path is not None:
        feature_importances.to_csv(csv_path)
    
    if png_path is not None:
        feature_importances.plot(kind='bar', figsize=(20,20))
        plt.savefig(png_path, bbox_inches='tight')
    
##################################################
# 特徴量の重要度を出力する(xgboostの決定木用)
##################################################
def output_importance_of_feature_for_xgboost(fscore, csv_path):
    
    feature_importances = pd.Series(fscore, name='Importance')
    feature_importances = feature_importances.sort_values(ascending=False)
    feature_importances.to_csv(csv_path)
    
