from .generic_propulsion_component import GenericPropulsionComponent
import numpy as np

class Turbine(GenericPropulsionComponent):
    def __init__(self):
        super().__init__()
        self.efficiency = 0.90
        self.specific_heat_ratio = 1.40
        self.polynomial_rotation_efficiency = [-6.7490E-02, 2.5640E-01, 8.1153E-01]
        self.polynomial_rotation_pressure_ratio = [1]

    def set_pressure_ratio(self, pressure_ratio):
        self.pressure_ratio = pressure_ratio
    
    def get_pressure_ratio(self):
        return self.pressure_ratio

    def set_cp(self, cp):
        self.cp = cp

    def get_cp(self):
        return self.cp

    def set_polynomial_rotation_pressure_ratio(self, polynomial_rotation_pressure_ratio):
        self.polynomial_rotation_pressure_ratio = polynomial_rotation_pressure_ratio
    
    def get_polynomial_rotation_pressure_ratio(self):
        return self.polynomial_rotation_pressure_ratio
    
    def get_rotation_pressure_ratio(self, rotation):
        polynomial_rotation_pressure_ratio = self.get_polynomial_rotation_pressure_ratio()
        baseline_pressure_ratio = self.get_pressure_ratio()
        multiplier = np.polyval(polynomial_rotation_pressure_ratio, rotation)

        rotation_pressure_ratio = baseline_pressure_ratio * multiplier

        return rotation_pressure_ratio
