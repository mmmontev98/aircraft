import sys

from .propulsion_methods import SetFunctions
from .propulsion_parameters import PropulsionParameters
from .turbofan_compute import TurboFanCompute
from .turbojet_compute import TurboJetCompute
from .ramjet_compute import RamJetCompute
from .propulsion_results import PropulsionResults

class PropulsionWrapper(SetFunctions):
    def __init__(self, aircraft_module):
        self.parameters = PropulsionParameters(aircraft_module)
        super().__init__(self.parameters)
        self.results = PropulsionResults()

    def initialize(self, propulsion_module_string=None):
        if propulsion_module_string is None:
            propulsion_module_string = self.parameters.get_propulsion_module_string()
        if propulsion_module_string == 'TurboFan':
            self.propulsion_compute = TurboFanCompute(self.parameters)
        elif propulsion_module_string == 'TurboJet':
            self.propulsion_compute = TurboJetCompute(self.parameters)
        elif propulsion_module_string == 'RamJet':
            self.propulsion_compute = RamJetCompute(self.parameters)
        else:
            print("[ERROR] No such module, %s, version exists for Propulsion()" % propulsion_module_string)
            sys.exit()
        
        self.propulsion_compute.set_results(self.results)
        self.propulsion_compute.initialize()

    def compute(self):
        self.propulsion_compute.compute()

    def get_parameters(self):
        return self.parameters

    def get_results(self):
        return self.results