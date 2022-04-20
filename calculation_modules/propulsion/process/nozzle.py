from .generic_propulsion_process import GenericPropulsionProcess
from ..propulsion_parameters import PropulsionParameters

class NozzleProcess(GenericPropulsionProcess):
    def __init__(self, parameters: PropulsionParameters, component):
        self.component_module = component
        self.rotation = parameters.get_compressor_rotation()
        self.rotation_flag = parameters.get_rotation_flag()
        self.P_out = parameters.get_outlet_pressure()
        self.R_mean = parameters.get_propulsion_module().get_mean_R()


    def get_thermodynamic_state(self, inlet_temperature, inlet_pressure):
        outlet_pressure = inlet_pressure
        outlet_temperature = inlet_temperature

        return (outlet_temperature, outlet_pressure)
    
    def get_outlet_speed(self, inlet_temperature, inlet_pressure):
        specific_heat_ratio = self.component_module.get_specific_heat_ratio()
        exp = (specific_heat_ratio - 1)/specific_heat_ratio
        efficiency = self.get_rotation_efficiency(self.rotation)

        u_s = (2*efficiency*(1/exp)*self.R_mean*inlet_temperature*(1 - (self.P_out/inlet_pressure)**exp))**(1/2)

        return u_s
    