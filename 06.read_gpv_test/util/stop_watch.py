# coding: utf-8

import time

##################################################
# 処理時間計測クラス
##################################################
class StopWatch:
    
    ##################################################
    # コンストラクタ
    ##################################################
    def __init__(self):
        self._start_time = None
        self._stop_time = None
    
    ##################################################
    # 処理時間計測開始
    ##################################################
    def start(self):
        self._start_time = time.time()
        return self
        
    ##################################################
    # 処理時間計測停止
    ##################################################
    def stop(self):
        self._stop_time = time.time()
        return self
    
    ##################################################
    # 経過時間
    ##################################################
    @property
    def elapsed_sec(self):
        if self._stop_time is None:
            self.stop()
        return (self._stop_time - self._start_time)
    
    ##################################################
    # 経過時間を表示する
    ##################################################
    def print_elapsed_sec(self, caption):
        elapsed_sec = self.elapsed_sec
        print('{0:s}: {1:.3f}[sec]'.format(caption, elapsed_sec))
        

    #@elapsed_sec.getter
    #def elapsed_sec(self):
    #    return self.__name    