import numpy as np
from .generic_propulsion_component import GenericPropulsionComponent

class Booster(GenericPropulsionComponent):
    def __init__(self):
        super().__init__()
        self.efficiency = 0.90
        self.specific_heat_ratio = 1.40
        self.delta_p = 0
        self.polynomial_rotation_pressure_ratio = [4.8967E-01, -4.3317E-02, 5.6846E-01]
        self.polynomial_rotation_efficiency = [1]
        
    def set_outlet_temperature(self, outlet_temperature):
        self.outlet_temperature = outlet_temperature
    
    def set_delta_p(self, delta_p):
        self.delta_p = delta_p
    
    def set_cp(self, cp):
        self.cp = cp
    
    def set_PCI(self, PCI):
        self.PCI = PCI
    
    def get_outlet_temperature(self):
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