from aircraft_modules.propulsion.components.combustor import Combustor
from aircraft_modules.propulsion.propulsion import Propulsion
from .generic_propulsion_process import GenericPropulsionProcess
from ..propulsion_parameters import PropulsionParameters

class CombustionProcess(GenericPropulsionProcess):
    def __init__(self, parameters: PropulsionParameters, component):
        self.component_module: Combustor = component
        self.rotation = parameters.get_compressor_rotation()
        self.rotation_flag = parameters.get_rotation_flag()

    def get_thermodynamic_state(self, inlet_temperature, inlet_pressure):
        specific_heat_ratio = self.component_module.get_specific_heat_ratio()
        exp = (specific_heat_ratio - 1)/specific_heat_ratio
        
        deltaP = self.component_module.get_delta_p() * inlet_pressure
        outlet_pressure = inlet_pressure - deltaP
        
        outlet_temperature_s = self.get_rotation_outlet_temperature(self.rotation)
        self.outlet_temperature = outlet_temperature_s * (outlet_pressure/inlet_pressure)**exp
        self.inlet_temperature = inlet_temperature

        return (self.outlet_temperature, outlet_pressure)

    def get_fuel_air_ratio(self):
        efficiency = self.get_rotation_efficiency(self.rotation)
        PCI = self.component_module.get_PCI()
        cp = self.component_module.get_cp()
        
        temperature_ratio = self.outlet_temperature/self.inlet_temperature
        fuel_air_ratio = (temperature_ratio - 1)/(efficiency*PCI/(cp*self.inlet_temperature) - temperature_ratio)

        return fuel_air_ratio

    def get_rotation_outlet_temperature(self, rotation):
        baseline_outlet_temperature = self.get_baseline_outlet_temperature()
        if not self.rotation_flag:
            return baseline_outlet_temperature

        return self.component_module.get_rotation_outlet_temperature(rotation)
        
    def get_baseline_outlet_temperature(self):
        return self.component_module.get_outlet_temperature()