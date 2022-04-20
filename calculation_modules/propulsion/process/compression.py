from aircraft_modules.propulsion.components import GenericPropulsionComponent
from .generic_propulsion_process import GenericPropulsionProcess
from ..propulsion_parameters import PropulsionParameters

class CompressionProcess(GenericPropulsionProcess):
    def __init__(self, parameters: PropulsionParameters, component):
        self.component_module : GenericPropulsionComponent  = component
        self.rotation = parameters.get_compressor_rotation()
        self.rotation_flag = parameters.get_rotation_flag()
    
    def get_thermodynamic_state(self, inlet_temperature, inlet_pressure):
        pressure_ratio = self.get_rotation_pressure_ratio(self.rotation)
        air_passage_ratio = self.get_rotation_air_passage_ratio(self.rotation)
        efficiency = self.get_rotation_efficiency(self.rotation)
        specific_heat_ratio = self.component_module.get_specific_heat_ratio()
        
        outlet_pressure = inlet_pressure*pressure_ratio
        exp = (specific_heat_ratio - 1)/specific_heat_ratio
        outlet_temperature = inlet_temperature*(1 + (1/efficiency)*(pressure_ratio**(exp) - 1))

        self.delta_T = (air_passage_ratio+1)*(outlet_temperature - inlet_temperature)
                

        return (outlet_temperature, outlet_pressure)
    
    def get_rotation_pressure_ratio(self, rotation):
        baseline_pressure_ratio = self.get_baseline_pressure_ratio()
        if not self.rotation_flag:
            return baseline_pressure_ratio

        return self.component_module.get_rotation_pressure_ratio(rotation)

    def get_delta_T(self):
        return self.delta_T
    
    def get_rotation(self, rotation):
        rotation = self.component_module.get_rotation(rotation)
        
        return rotation

    def get_baseline_pressure_ratio(self):
        return self.component_module.get_pressure_ratio()

    def get_baseline_air_passage_ratio(self):
        return self.component_module.get_air_passage_ratio()
    
    def get_rotation_air_passage_ratio(self, rotation):
        baseline_air_passage_ratio = self.get_baseline_air_passage_ratio()
        if not self.rotation_flag:
            return baseline_air_passage_ratio
        
        return self.component_module.get_rotation_air_passage_ratio(rotation)
