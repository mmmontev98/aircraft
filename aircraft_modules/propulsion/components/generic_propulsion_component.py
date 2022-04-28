import numpy as np
class GenericPropulsionComponent():
    def __init__(self):
        self.linked_component = None

    def set_specific_heat_ratio(self, specific_heat_ratio):
        self.specific_heat_ratio = specific_heat_ratio

    def set_efficiency(self, efficiency):
        self.efficiency = efficiency

    def set_polynomial_rotation_efficiency(self, polynomial_rotation_efficiency):
        self.polynomial_rotation_efficiency = polynomial_rotation_efficiency

    def get_efficiency(self):
        return self.efficiency

    def get_specific_heat_ratio(self):
        return self.specific_heat_ratio
    
    def set_stream_id(self, stream_id):
        self.stream_id = stream_id

    def get_stream_id(self):
        return self.stream_id
    
    def set_name(self, name):
        self.name = name
    
    def get_name(self):
        return self.name

    def set_type(self, type):
        self.type = type
    
    def get_type(self):
        return self.type

    def set_linked_component(self, linked_component):
        self.linked_component = linked_component
    
    def get_linked_component(self):
        return self.linked_component

    def get_polynomial_rotation_efficiency(self):
            return self.polynomial_rotation_efficiency
    
    def get_rotation_efficiency(self, rotation):
        polynomial_rotation_efficiency = self.get_polynomial_rotation_efficiency()
        baseline_efficiency = self.get_efficiency()
        multiplier = np.polyval(polynomial_rotation_efficiency, rotation)

        if multiplier > 1:
            multiplier = 1
        
        rotation_efficiency = baseline_efficiency * multiplier        


        return rotation_efficiency


    def load_component(self, component_dict:dict):
        for parameter in component_dict:
            getattr(self, 'set_' + parameter)(component_dict[parameter])

