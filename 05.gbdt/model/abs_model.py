# coding: utf-8

from abc import ABCMeta, abstractmethod

class AbsModel(metaclass=ABCMeta):
    
    def __init__(self, run_fold_name, params):
        self.run_fold_name = run_fold_name
        self.params = params

    @abstractmethod
    def train(self, train_x, train_y, validate_x, validate_y):
        raise NotImplementedError()
        
    @abstractmethod
    def predict(self, test_x):
        raise NotImplementedError()
        
    @abstractmethod
    def save_model(self):
        raise NotImplementedError()
        
    @abstractmethod
    def load_model(self):
        raise NotImplementedError()
        
        