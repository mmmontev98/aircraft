from abc import ABC, abstractclassmethod


class generic_module(ABC):
    def __init__(self, module_name):
        self.module_name = module_name

    # @abstractclassmethod
    # def initialize():
    #     '''bla'''
    
    @abstractclassmethod
    def load_module():
        '''bla'''