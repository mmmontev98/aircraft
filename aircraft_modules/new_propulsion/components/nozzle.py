from .generic_propulsion_component import GenericPropulsionComponent
import numpy as np

class Nozzle(GenericPropulsionComponent):
    def __init__(self):
        super().__init__()
        self.efficiency = 0.90
        self.specific_heat_ratio = 1.40