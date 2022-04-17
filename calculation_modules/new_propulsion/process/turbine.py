from .generic_propulsion_process import GenericPropulsionProcess
from ..propulsion_parameters import PropulsionParameters

class TurbineProcess(GenericPropulsionProcess):
    def __init__(self, parameters: PropulsionParameters, component):
        self.parameters = parameters
        self.component_module = component
        self.T_a = parameters.get_temperature_a()
        self.P_a = parameters.get_pressure_a()
        self.rotation_flag = parameters.get_rotation_flag()
        self.rotation = parameters.get_compressor_rotation()

    def get_thermodynamic_state(self, inlet_temperature, inlet_pressure): #, delta_T_compression, component_rotation):
        linked_component = self.get_linked_component_process()
        delta_T_compression = linked_component.get_delta_T()
        
        component_rotation = linked_component.get_rotation(self.rotation)
        
        specific_heat_ratio = self.component_module.get_specific_heat_ratio()
        exp = specific_heat_ratio/(specific_heat_ratio - 1)
        efficiency = self.get_rotation_efficiency(component_rotation)


        outlet_temperature = inlet_temperature - delta_T_compression
        outlet_pressure = inlet_pressure*(1 - (1/efficiency)*(1 - outlet_temperature/inlet_temperature))**exp

        return (outlet_temperature, outlet_pressure)