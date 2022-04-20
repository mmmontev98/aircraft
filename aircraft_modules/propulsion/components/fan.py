from .generic_propulsion_component import GenericPropulsionComponent
import numpy as np

class Fan(GenericPropulsionComponent):
    def __init__(self):
        super().__init__()
        self.efficiency = 0.90
        self.specific_heat_ratio = 1.40
        self.polynomial_rotation_pressure_ratio = [[-0.00179, 0.00687, 0.5], [0, 0, 4.3317E-02], [0, 0.011, 0.53]]
        self.polynomial_rotation_fan_compressor = [1.4166E+00, - 4.0478E-01]
        self.polynomial_rotation_air_passage_ratio = [-8.3241E-01, 3.8824E-01, 1.4263E+00]
        self.polynomial_rotation_efficiency = [-6.6663, 17.752, - 17.469, 7.7181, - 0.32985]

    def set_pressure_ratio(self, pressure_ratio):
        self.pressure_ratio = pressure_ratio
    
    def get_pressure_ratio(self):
        return self.pressure_ratio

    def set_air_passage_ratio(self, air_passage_ratio):
        self.air_passage_ratio = air_passage_ratio
    
    def get_air_passage_ratio(self):
        return self.air_passage_ratio

    
    def set_polynomial_rotation_fan_compressor(self, polynomial_rotation_fan_compressor):
        self.polynomial_rotation_fan_compressor = polynomial_rotation_fan_compressor

    def get_polynomial_rotation_fan_compressor(self):
        return self.polynomial_rotation_fan_compressor

    def get_rotation_fan(self, rotation):
        polynomial_rotation_fan_compressor = self.get_polynomial_rotation_fan_compressor()
        multiplier = np.polyval(polynomial_rotation_fan_compressor, rotation)

        rotation_fan = rotation * multiplier

        return rotation_fan



    def set_polynomial_rotation_pressure_ratio(self, polynomial_rotation_pressure_ratio):
        self.polynomial_rotation_pressure_ratio = polynomial_rotation_pressure_ratio
    
    def get_polynomial_rotation_pressure_ratio(self):
        return self.polynomial_rotation_pressure_ratio
    
    def get_rotation_pressure_ratio(self, rotation):
        polynomial_rotation_pressure_ratio = self.get_polynomial_rotation_pressure_ratio()
        baseline_pressure_ratio = self.get_pressure_ratio()
        baseline_air_passage_ratio = self.get_air_passage_ratio()
        fan_rotation = self.get_rotation_fan(rotation)

        ABC_constants = []
        for ABC_polynomial in polynomial_rotation_pressure_ratio:
           ABC_constants.append(np.polyval(ABC_polynomial, baseline_air_passage_ratio))

        multiplier = np.polyval(ABC_constants, fan_rotation)

            
        rotation_pressure_ratio = baseline_pressure_ratio * multiplier


        return rotation_pressure_ratio

    def set_polynomial_rotation_air_passage_ratio(self, polynomial_rotation_air_passage_ratio):
        self.polynomial_rotation_air_passage_ratio = polynomial_rotation_air_passage_ratio
    
    def get_polynomial_rotation_air_passage_ratio(self):
        return self.polynomial_rotation_air_passage_ratio
    
    def get_rotation_air_passage_ratio(self, rotation):
        polynomial_rotation_air_passage_ratio = self.get_polynomial_rotation_air_passage_ratio()
        baseline_air_passage_ratio = self.get_air_passage_ratio()
        fan_rotation = self.get_rotation(rotation)
        multiplier = np.polyval(polynomial_rotation_air_passage_ratio, fan_rotation)

        

        rotation_air_passage_ratio = baseline_air_passage_ratio * multiplier

        return rotation_air_passage_ratio

    def get_rotation(self, rotation):
        fan_rotation = self.get_rotation_fan(rotation)
        return fan_rotation