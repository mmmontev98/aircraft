from aircraft_modules.new_propulsion.propulsion import Propulsion
from ..generic_propulsion_process import GenericPropulsionProcess
from ...propulsion_parameters import PropulsionParameters

class PostCombustionProcess(GenericPropulsionProcess):
    def __init__(self, parameters: PropulsionParameters, component):
        self.component_module = component
        self.rotation = parameters.get_compressor_rotation()
        self.rotation_flag = parameters.get_rotation_flag()

    def get_thermodynamic_state(self, inlet_temperature, inlet_pressure):
        specific_heat_ratio = self.component_module.get_specific_heat_ratio()
        exp = (specific_heat_ratio - 1)/specific_heat_ratio
        
        deltaP = self.component_module.get_delta_p()
        outlet_pressure = inlet_pressure - deltaP
        
        outlet_temperature_s = self.get_rotation_outlet_temperature(self.rotation)
        outlet_temperature = outlet_temperature_s * (outlet_pressure/inlet_pressure)**exp

        fuel_air_ratio = self.get_fuel_air_ratio(inlet_temperature, outlet_temperature)

        return (outlet_temperature, outlet_pressure, fuel_air_ratio)

    def get_fuel_air_ratio(self, inlet_temperature, outlet_temperature):
        efficiency = self.get_rotation_efficiency(self.rotation)
        PCI = self.component_module.get_PCI()
        cp = self.component_module.get_cp()
        
        temperature_ratio = outlet_temperature/inlet_temperature
        fuel_air_ratio = (temperature_ratio - 1)/(efficiency*PCI/(cp*inlet_temperature) - temperature_ratio)

        return fuel_air_ratio

    
    def get_rotation_efficiency(self, rotation):
        baseline_efficiency = self.get_baseline_efficiency()
        if not self.rotation_flag:
            return baseline_efficiency
        
        multiplier = 1.0
        rotation_efficiency = multiplier * baseline_efficiency
        return rotation_efficiency

    def get_rotation_outlet_temperature(self, rotation):
        baseline_outlet_temperature = self.get_baseline_outlet_temperature()
        if not self.rotation_flag:
            return baseline_outlet_temperature
        
        multiplier = 1.0
        rotation_outlet_temperature = multiplier * baseline_outlet_temperature
        
        return rotation_outlet_temperature
    
    def get_baseline_efficiency(self):
        return self.component_module.get_efficiency()

    def get_baseline_outlet_temperature(self):
        return self.component_module.get_outlet_temperature()