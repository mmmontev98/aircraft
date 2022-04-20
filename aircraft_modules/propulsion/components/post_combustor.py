from .generic_propulsion_component import GenericPropulsionComponent
import numpy as np

class PostCombustor(GenericPropulsionComponent):
    def __init__(self):
        super().__init__()
        self.efficiency = 0.90
        self.specific_heat_ratio = 1.40
        self.polynomial_rotation_outlet_temperature = [8.1821E-01, - 2.2401E-01, 4.1842E-01]
        self.polynomial_rotation_efficiency = [1.1630E+00, - 3.0851E+00, 2.7312E+00, 1.9130E-01]

    def set_outlet_temperature(self, outlet_temperature):
        self.outlet_temperature = outlet_temperature
    
    def set_delta_p(self, delta_p):
        self.delta_p = delta_p
    
    def set_cp(self, cp):
        self.cp = cp
    
    def set_PCI(self, PCI):
        self.PCI = PCI
    
    def get_outlet_temperature(self, outlet_temperature):
        return self.outlet_temperature
    
    def get_delta_p(self):
        return self.delta_p
    
    def get_cp(self):
        return self.cp
    
    def get_PCI(self):
        return self.PCI

    def set_polynomial_rotation_outlet_temperature(self, polynomial_rotation_outlet_temperature):
        self.polynomial_rotation_outlet_temperature = polynomial_rotation_outlet_temperature
    
    def get_polynomial_rotation_outlet_temperature(self):
        return self.polynomial_rotation_outlet_temperature
    
    def get_rotation_outlet_temperature(self, rotation):
        polynomial_rotation_outlet_temperature = self.get_polynomial_rotation_outlet_temperature()
        baseline_outlet_temperature = self.get_outlet_temperature()
        multiplier = np.polyval(polynomial_rotation_outlet_temperature, rotation)

        rotation_outlet_temperature = baseline_outlet_temperature * multiplier

        return rotation_outlet_temperature