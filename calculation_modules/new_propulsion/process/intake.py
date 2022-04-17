from .generic_propulsion_process import GenericPropulsionProcess
from ..propulsion_parameters import PropulsionParameters

class IntakeProcess(GenericPropulsionProcess):
    def __init__(self, parameters: PropulsionParameters, component):
        self.component_module = component
        self.mach = parameters.get_mach()
        self.rotation = parameters.get_compressor_rotation()
        self.rotation_flag = parameters.get_rotation_flag()


    def get_thermodynamic_state(self, inlet_temperature, inlet_pressure):
        specific_heat_ratio = self.component_module.get_specific_heat_ratio()
        efficiency = self.get_rotation_efficiency(self.rotation)
        exp = specific_heat_ratio/(specific_heat_ratio - 1)
        
        outlet_temperature = inlet_temperature*(1 + ((specific_heat_ratio - 1)/2)*self.mach**2)
        outlet_pressure = inlet_pressure*(1 + efficiency*(outlet_temperature/inlet_temperature -1))**(exp)
        
        return (outlet_temperature, outlet_pressure)