# coding: utf-8

from abc import ABCMeta, abstractmethod

class AbsLoader(metaclass=ABCMeta):
    
    def __init__(self, base_dir, temp_dirname, input_dirname):
        self.base_dir = base_dir
        self.temp_dirname = temp_dirname
        self.input_dirname = input_dirname

    @abstractmethod
    def load(self):
        raise NotImplementedError()
        
