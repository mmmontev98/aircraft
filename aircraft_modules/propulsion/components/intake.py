from .generic_propulsion_component import GenericPropulsionComponent
import numpy as np

class Intake(GenericPropulsionComponent):
    def __init__(self):
        super().__init__()
        self.efficiency = 0.90
        self.specific_heat_ratio = 1.40
        self.polynomial_rotation_efficiency = [1]