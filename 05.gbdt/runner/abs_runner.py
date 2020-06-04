# coding: utf-8

from abc import ABCMeta, abstractmethod

class AbsRunner(metaclass=ABCMeta):
    
    def __init__(self, run_name, model, params):
        self.run_name = run_name
        self.model = model
        self.params = params

    @abstractmethod
    def run_train_fold(self, fold):
        raise NotImplementedError()
        
    @abstractmethod
    def run_train_cv(self):
        raise NotImplementedError()
        
    @abstractmethod
    def run_predict_cv(self):
        raise NotImplementedError()
        
    @abstractmethod
    def run_train_all(self):
        raise NotImplementedError()
    
    @abstractmethod
    def run_predict_all(self):
        raise NotImplementedError()
        
        