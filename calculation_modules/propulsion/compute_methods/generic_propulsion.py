from abc import abstractclassmethod, ABC
import numpy as np

from ..process import ProcessStream

from ..propulsion_parameters import PropulsionParameters
from ..propulsion_results import PropulsionResults

class GenericPropulsionSubmodule(ABC):
    def __init__(self, parameters: PropulsionParameters):
        self.parameters = parameters
        self.propulsion_module = parameters.get_propulsion_module()
        self.process_streams = ProcessStream(parameters)
    
    @abstractclassmethod
    def compute_thermal_efficiency():
        ''' return thermal_efficiency'''
      
    @abstractclassmethod
    def compute_propulsion_efficiency():
        '''return propulsion_efficiency'''

    @abstractclassmethod
    def compute_total_efficiency():
        '''return total_efficiency'''
    
    @abstractclassmethod
    def compute_specific_thrust():
        '''return specific_thrust'''
    
    @abstractclassmethod
    def compute():
        '''Compute thermodynamics states and performance parameters'''

    def initialize(self):
        component_streams = self.propulsion_module.get_component_stream()
        self.process_streams.set_component_stream(component_streams)
        self.process_streams.initialize()

    def compute_thermodynamic_states(self):
        T_a = self.parameters.get_temperature_a()
        P_a = self.parameters.get_pressure_a()
        (dict_T_0, 
        dict_P_0, 
        dict_outlet_speed, 
        dict_fuel_air_ratio) = self.process_streams.compute_stream(T_a, P_a)

        self.results.set_T_0(dict_T_0)
        self.results.set_P_0(dict_P_0)
        self.results.set_outlet_speed(dict_outlet_speed)
        self.results.set_fuel_air_ratio(dict_fuel_air_ratio)
        return dict_outlet_speed, dict_fuel_air_ratio


    def get_rotation_mass_flow(self, rotation):
        corrected_mass_flow = self.get_corrected_mass_flow()
        if not self.parameters.get_rotation_flag():
            return corrected_mass_flow
        
        polynomial_rotation_mass_flow = self.parameters.get_polynomial_rotation_mass_flow()
        multiplier = np.polyval(polynomial_rotation_mass_flow, rotation)
        rotation_mass_flow = corrected_mass_flow * multiplier

        return rotation_mass_flow
        
    def get_corrected_mass_flow(self):
        Ta = self.parameters.get_temperature_a()
        Pa = self.parameters.get_pressure_a()
        baseline_mass_flow = self.parameters.get_mass_flow()
        corrected_mass_flow = baseline_mass_flow * (288.15/101.325) * (Pa/Ta)

        return corrected_mass_flow
        

    def get_rotation_air_passage_ratio(self, rotation):
        fan_module = self.parameters.get_fan_module()
        baseline_air_passage_ratio = fan_module.get_air_passage_ratio()
        if not self.parameters.get_rotation_flag():
            return baseline_air_passage_ratio

        return fan_module.get_rotation_air_passage_ratio(rotation)

    def set_results(self, results: PropulsionResults):
        self.results = results
    


    