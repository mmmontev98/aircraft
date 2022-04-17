from ..generic_propulsion_process import GenericPropulsionProcess
from ...propulsion_parameters import PropulsionParameters

class BoosterProcess(GenericPropulsionProcess):
    def __init__(self, parameters: PropulsionParameters, component):
        self.component_module = component
        self.rotation = parameters.get_compressor_rotation()
        self.rotation_flag = parameters.get_rotation_flag()
    
    def get_thermodynamic_state(self, inlet_temperature, inlet_pressure):
        pressure_ratio = self.get_rotation_pressure_rotation(self.rotation)
        efficiency = self.get_rotation_efficiency(self.rotation)
        specific_heat_ratio = self.component_module.get_specific_heat_ratio()
        
        outlet_pressure = inlet_pressure*pressure_ratio
        exp = (specific_heat_ratio - 1)/specific_heat_ratio
        outlet_temperature = inlet_temperature*(1 + (1/efficiency)*(pressure_ratio**(exp) - 1))
        
        return (outlet_temperature, outlet_pressure) 
    
    def get_fan_rotation(self, rotation):
        multiplier = 1.4166E+00*rotation - 4.0478E-01
        return multiplier*rotation

    def get_rotation_efficiency(self, rotation):
        
        baseline_efficiency = self.get_baseline_efficiency()
        if not self.rotation_flag:
            return baseline_efficiency
        
        multiplier = 1.0
        
        rotation_efficiency = multiplier * baseline_efficiency
        return rotation_efficiency

    def get_rotation_pressure_rotation(self, rotation):
        baseline_pressure_ratio = self.get_baseline_pressure_ratio()
        if not self.rotation_flag:
            return baseline_pressure_ratio
        
        fan_rotation = self.get_fan_rotation(rotation)
        
        multiplier = 4.8967E-01*fan_rotation**2 - 4.3317E-02*fan_rotation + 5.6846E-01
        
        rotation_pressure_ratio = multiplier * baseline_pressure_ratio
        
        return rotation_pressure_ratio
    
    def get_baseline_efficiency(self):
        return self.component_module.get_efficiency()

    def get_baseline_pressure_ratio(self):
        return self.component_module.get_pressure_ratio()
