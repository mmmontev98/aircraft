from .generic_propulsion_component import GenericPropulsionComponent
import numpy as np

class Nozzle(GenericPropulsionComponent):
    def __init__(self):
        super().__init__()
        self.efficiency = 0.90
        self.specific_heat_ratio = 1.40
        self.mean_R = 285
        
    def set_mean_R(self, mean_R):
        self.mean_R = mean_R
    
    def get_mean_R(self):
        return self.mean_R
    