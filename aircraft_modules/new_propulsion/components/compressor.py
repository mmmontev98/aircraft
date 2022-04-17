from .generic_propulsion_component import GenericPropulsionComponent
import numpy as np

class Compressor(GenericPropulsionComponent):
    def __init__(self):
        super().__init__()
        self.efficiency = 0.90
        self.specific_heat_ratio = 1.40
        self.pressure_ratio = 1
        self.air_passage_ratio = 0
        self.polynomial_rotation_pressure_ratio = [-6.0730E+00, 1.4821E+01, - 1.0042E+01, 2.2915E+00]
        self.polynomial_rotation_efficiency = [-1.1234E+00, 2.1097E+00, 1.8617]

    def set_pressure_ratio(self, pressure_ratio):
        self.pressure_ratio = pressure_ratio
    
    def get_pressure_ratio(self):
        return self.pressure_ratio
    
    def get_rotation_air_passage_ratio(self, rotation):
        return self.get_air_passage_ratio()
    
    def get_air_passage_ratio(self):
        return self.air_passage_ratio

    def set_air_passage_ratio(self, air_passage_ratio):
        self.air_passage_ratio = air_passage_ratio

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

    def get_rotation(self, rotation):
        return rotation