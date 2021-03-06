from .generic_propulsion import GenericPropulsion
from .components import Fan
from .components import ComponentStream
import json

class Propulsion(GenericPropulsion):
    def __init__(self):
        self.component_module_list = []
        self.fan = None
        self.component_streams = ComponentStream()
    
    def set_specific_heat_ratio_a(self, specific_heat_ratio_a):
        self.specific_heat_ratio_a = specific_heat_ratio_a
    
    def set_mean_R(self, mean_R):
        self.mean_R = mean_R
    
    def set_cp(self, cp):
        self.cp = cp
    
    def set_PC(self, PC):
        self.PC = PC
    
    def set_air_passage_ratio(self, air_passage_ratio):
        self.fan.set_air_passage_ratio(air_passage_ratio)

    def set_propeller_efficiency(self, propeller_efficiency):
        self.propeller_efficiency = propeller_efficiency

    def set_gearbox_power_ratio(self, gearbox_power_ratio):
        self.gearbox_power_ratio = gearbox_power_ratio
    
    def get_gearbox_power_ratio(self):
        return self.gearbox_power_ratio
    
    def get_propeller_efficiency(self):
        return self.propeller_efficiency
    
    def get_air_passage_ratio(self):
        return self.fan.get_air_passage_ratio()
    
    def get_specific_heat_ratio_a(self):
        return self.specific_heat_ratio_a
    
    def get_mean_R(self):
        return self.mean_R
     
    def get_cp(self):
        return self.cp
    
    
    def get_PC(self):
        return self.PC

    def get_component_stream(self):
        return self.component_streams

    def get_fan_module(self) -> Fan:
        return self.fan

    def get_component(self, stream_id, component_name):
        return self.get_component_stream().get_component(stream_id, component_name)

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
