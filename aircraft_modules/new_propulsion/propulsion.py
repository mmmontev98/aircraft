from .generic_propulsion import GenericPropulsion
from .components import Fan
from .components import ComponentStream
import json

class Propulsion(GenericPropulsion):
    def __init__(self):
        self.component_module_list = []
        self.component_streams = ComponentStream()
    
    def set_specific_heat_ratio_a(self, specific_heat_ratio_a):
        self.specific_heat_ratio_a = specific_heat_ratio_a
    
    def set_mean_R(self, mean_R):
        self.mean_R = mean_R
    
    def set_cp(self, cp):
        self.cp = cp
    
    def set_PC(self, PC):
        self.PC = PC
    
    def get_specific_heat_ratio_a(self):
        return self.specific_heat_ratio_a
    
    def get_mean_R(self):
        return self.mean_R
     
    def get_cp(self):
        return self.cp
    
    def get_air_passage_ratio(self):
        return self.fan.get_air_passage_ratio()
    
    def get_PC(self):
        return self.PC

    def get_component_stream(self):
        return self.component_streams

    def get_fan_module(self) -> Fan:
        return self.fan

    def add_component(self, component):
        self.component_streams.add_component(component)
    
    def set_components(self, components_dict):
        for component_name in components_dict:
            component_dict = components_dict[component_name]
            component_type = component_dict["type"]
            component = self.create_component_module(component_type)
            component.set_name(component_name)
            component.load_component(component_dict)
            self.add_component(component)
    
    def load_module(self, propulsion_module_dict:dict):
        for parameter in propulsion_module_dict:
            getattr(self, 'set_' + parameter)(propulsion_module_dict[parameter])

    def get_module_dictionary(self, module_information):
        module_dir_path = './database/propulsion/' + module_information + '/'

        with open(module_dir_path + 'propulsion.json', 'r') as file:
            module_dict = json.load(file)

        return module_dict
