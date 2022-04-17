import sys
from .components import GenericPropulsionComponent
from .components import Booster, Combustor, Compressor, Fan
from .components import Intake, Nozzle, PostCombustor, Turbine
from ..generic_module import generic_module

class GenericPropulsion(generic_module):  
    def create_component_module(self, component_type) -> GenericPropulsionComponent:
        if component_type == 'booster':
            component_module = Booster()
        elif component_type == 'combustor':
            component_module = Combustor()
        elif component_type == 'compressor':
            component_module = Compressor()
        elif component_type == 'fan':
            component_module = Fan()
            self.fan = component_module
        elif component_type == 'intake':
            component_module = Intake()
        elif component_type == 'nozzle':
            component_module = Nozzle()
        elif component_type == 'post_combustor':
            component_module = PostCombustor()
        elif component_type == 'turbine':
            component_module = Turbine()        
        else:
            print("[ERROR] No such component, %s, version exists for Propulsion()" % component_type)
            sys.exit()
        
        return component_module