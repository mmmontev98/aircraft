from aircraft_modules.new_propulsion.components import Fan
from ..generic_propulsion_process import GenericPropulsionProcess
from ...propulsion_parameters import PropulsionParameters

class FanProcess(GenericPropulsionProcess):
    def __init__(self, parameters: PropulsionParameters, component):
        self.component_module : Fan = component
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
    
    # def get_rotation_efficiency(self, rotation):
    #     baseline_efficiency = self.get_baseline_efficiency()
    #     if not self.rotation_flag:
    #         return baseline_efficiency
        
        # fan_rotation = self.get_fan_rotation(rotation)

        # multiplier = -6.6663*fan_rotation**4 + 17.752*fan_rotation**3- 17.469*fan_rotation**2 + 7.7181*fan_rotation - 0.32985

        # rotation_efficiency = multiplier * baseline_efficiency
        # return rotation_efficiency

    def get_rotation_pressure_ratio(self, rotation):
        baseline_pressure_ratio = self.get_baseline_pressure_ratio()
        if not self.rotation_flag:
            return baseline_pressure_ratio

        return self.component_module.get_rotation_pressure_ratio(rotation)
        
        # B_baseline = self.component_module.get_air_passage_ratio()
        # fan_rotation = self.get_fan_rotation(rotation)

        # A = -0.00179*(B_baseline)**2 + 0.00687*(B_baseline) + 0.5
        # B = - 4.3317E-02
        # C = 0.011*(B_baseline) + 0.53        
        # multiplier = A*fan_rotation**2 + B*fan_rotation + C
        
        # rotation_pressure_ratio = multiplier * baseline_pressure_ratio
        
        # return rotation_pressure_ratio
    
    # def get_fan_rotation(self, rotation):
    #     multiplier = 1.4166E+00*rotation - 4.0478E-01
    #     return multiplier*rotation
    
    def get_delta_T(self):
        return self.delta_T
    
    def get_rotation(self, rotation):
        fan_rotation = self.component_module.get_rotation(rotation)

        return fan_rotation
    
    # def get_baseline_efficiency(self):
    #     return self.component_module.get_efficiency()

    def get_baseline_pressure_ratio(self):
        return self.component_module.get_pressure_ratio()
    
    def get_baseline_air_passage_ratio(self):
        return self.component_module.get_air_passage_ratio()
    
    def get_rotation_air_passage_ratio(self, rotation):
        baseline_air_passage_ratio = self.get_baseline_air_passage_ratio()
        if not self.rotation_flag:
            return baseline_air_passage_ratio
        
        return self.component_module.get_rotation_air_passage_ratio(rotation)
        
        
        # fan_rotation = self.get_fan_rotation(rotation)
        
    
        # multiplier = -8.3241E-01*fan_rotation**2 + 3.8824E-01*fan_rotation + 1.4263E+00

        # rotation_air_passage_ratio = multiplier * baseline_air_passage_ratio
        
        # return rotation_air_passage_ratio

