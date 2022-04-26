from .generic_propulsion_process import GenericPropulsionProcess
from ..propulsion_parameters import PropulsionParameters

class ExpansionProcess(GenericPropulsionProcess):
    def __init__(self, parameters: PropulsionParameters, component):
        super().__init__()
        self.parameters = parameters
        self.component_module = component
        self.T_a = parameters.get_temperature_a()
        self.P_a = parameters.get_pressure_a()
        self.rotation_flag = parameters.get_rotation_flag()
        self.rotation = parameters.get_compressor_rotation()

    def get_thermodynamic_state(self, inlet_temperature, inlet_pressure): #, delta_T_compression, component_rotation):
        specific_heat_ratio = self.component_module.get_specific_heat_ratio()
        exp = (specific_heat_ratio - 1)/specific_heat_ratio
        

        linked_component = self.get_linked_component_process()
        if linked_component is not None:
            component_rotation = linked_component.get_rotation(self.rotation)
            delta_T_compression = linked_component.get_delta_T()
            efficiency = self.get_rotation_efficiency(component_rotation)
            
            outlet_temperature = inlet_temperature - delta_T_compression
            outlet_pressure = inlet_pressure*(1 - (1/efficiency)*(1 - outlet_temperature/inlet_temperature))**(1/exp)
        
        else:
            efficiency = self.get_rotation_efficiency(self.rotation)
            pressure_ratio = self.get_rotation_pressure_ratio(self.rotation)
            cp = self.component_module.get_cp()
            
            outlet_pressure = inlet_pressure/pressure_ratio
            outlet_temperature = inlet_temperature*(1 - efficiency*(1 - (1/pressure_ratio)**exp))

            self.specific_work_turbine = (inlet_temperature - outlet_temperature)*(cp)

        return (outlet_temperature, outlet_pressure)

    def get_rotation_pressure_ratio(self, rotation):
        baseline_pressure_ratio = self.get_baseline_pressure_ratio()
        if not self.rotation_flag:
            return baseline_pressure_ratio

        return self.component_module.get_rotation_pressure_ratio(rotation)

    def get_baseline_pressure_ratio(self):
        return self.component_module.get_pressure_ratio()

    def get_specific_work(self):
        return self.specific_work_turbine

    