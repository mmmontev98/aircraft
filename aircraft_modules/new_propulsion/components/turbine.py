from .generic_propulsion_component import GenericPropulsionComponent
import numpy as np

class Turbine(GenericPropulsionComponent):
    def __init__(self):
        super().__init__()
        self.efficiency = 0.90
        self.specific_heat_ratio = 1.40
        self.polynomial_rotation_efficiency = [-6.7490E-02, 2.5640E-01, 8.1153E-01]
