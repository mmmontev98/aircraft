from aircraft_modules.new_propulsion.propulsion import Propulsion
from .generic_propulsion import GenericPropulsionSubmodule
from .propulsion_parameters import PropulsionParameters

class TurboFanCompute(GenericPropulsionSubmodule):
    def __init__(self, parameters: PropulsionParameters):
        super().__init__(parameters)
        self.parameters = parameters
        self.rotation = parameters.get_compressor_rotation()
        self.propulsion_module : Propulsion = parameters.get_aircraft_module().get_new_propulsion_module()

    def compute(self):
        dict_outlet_speed, dict_fuel_air_ratio = self.compute_thermodynamic_states()
        
        self.compute_performance_parameters(dict_outlet_speed, dict_fuel_air_ratio)

        
    def compute_performance_parameters(self, dict_outlet_speed, dict_fuel_air_ratio):
        aircraft_speed = self.parameters.get_aircraft_speed()
        
        list_outlet_speed = get_list_outlet_speed(dict_outlet_speed)
        total_fuel_air_ratio = get_total_fuel_air_ratio(dict_fuel_air_ratio)

        outlet_speed_hot_air = list_outlet_speed[0]
        outlet_speed_fan = list_outlet_speed[1]

        specific_thrust = self.compute_specific_thrust(aircraft_speed, outlet_speed_hot_air, outlet_speed_fan, total_fuel_air_ratio)
        TSFC = self.compute_TSFC(aircraft_speed, outlet_speed_hot_air, outlet_speed_fan, total_fuel_air_ratio)
        thermal_efficiency = self.compute_thermal_efficiency(aircraft_speed, outlet_speed_hot_air, outlet_speed_fan, total_fuel_air_ratio)
        propulsion_efficiency = self.compute_propulsion_efficiency(aircraft_speed, outlet_speed_hot_air, outlet_speed_fan, total_fuel_air_ratio)
        total_efficiency = self.compute_total_efficiency(aircraft_speed, outlet_speed_hot_air, outlet_speed_fan, total_fuel_air_ratio)

        self.results.set_specific_thrust(specific_thrust)
        self.results.set_TSFC(TSFC)
        self.results.set_thermal_efficiency(thermal_efficiency)
        self.results.set_propulsion_efficiency(propulsion_efficiency)
        self.results.set_total_efficiency(total_efficiency)
    

    def compute_specific_thrust(self, aircraft_speed, outlet_speed_hot_air, outlet_speed_fan, fuel_air_ratio):
        air_passage_ratio = self.get_rotation_air_passage_ratio(self.rotation)
        
        specific_thrust = (1 + fuel_air_ratio)*outlet_speed_hot_air - aircraft_speed
        specific_thrust = specific_thrust + air_passage_ratio*(outlet_speed_fan - aircraft_speed)
        return specific_thrust

    def compute_TSFC(self, aircraft_speed, outlet_speed_hot_air, outlet_speed_fan, fuel_air_ratio):
        specific_thrust = self.compute_specific_thrust(aircraft_speed, outlet_speed_hot_air, outlet_speed_fan, fuel_air_ratio)
        TSFC = fuel_air_ratio/specific_thrust
        return TSFC

    def compute_thermal_efficiency(self, aircraft_speed, outlet_speed_hot_air, outlet_speed_fan, fuel_air_ratio):
        PC = self.propulsion_module.get_PC()*1000
        outlet_speed_bar = self.compute_outlet_speed_bar(outlet_speed_hot_air, outlet_speed_fan, fuel_air_ratio)
        # air_passage_ratio = self.get_rotation_air_passage_ratio(self.rotation)

        kinetic_energy_power = (1 + fuel_air_ratio) * (outlet_speed_bar**2/2) - aircraft_speed**2/2
        fuel_combustion_power = fuel_air_ratio * PC
        thermal_efficiency = kinetic_energy_power/fuel_combustion_power

        return thermal_efficiency
    
    def compute_propulsion_efficiency(self, aircraft_speed, outlet_speed_hot_air, outlet_speed_fan, fuel_air_ratio):
        specific_thrust = self.compute_specific_thrust(aircraft_speed, outlet_speed_hot_air, outlet_speed_fan, fuel_air_ratio)
        outlet_speed_bar = self.compute_outlet_speed_bar(outlet_speed_hot_air, outlet_speed_fan, fuel_air_ratio)
        air_passage_ratio = self.get_rotation_air_passage_ratio(self.rotation)
        
        propulsion_power = (specific_thrust*aircraft_speed)
        kinetic_energy_power = (1 + fuel_air_ratio) * (outlet_speed_bar**2/2) - aircraft_speed**2/2
        propulsion_efficiency = propulsion_power / kinetic_energy_power

        return propulsion_efficiency
    
    def compute_outlet_speed_bar(self, outlet_speed_hot_air, outlet_speed_fan, fuel_air_ratio):
        air_passage_ratio = self.get_rotation_air_passage_ratio(self.rotation)

        term_hot_air = outlet_speed_hot_air * (1 + air_passage_ratio)
        term_cold_air = outlet_speed_fan * air_passage_ratio
        outlet_speed_bar = (term_hot_air + term_cold_air)/(1+air_passage_ratio+fuel_air_ratio)

        return outlet_speed_bar


    def compute_total_efficiency(self, aircraft_speed, outlet_speed_hot_air, outlet_speed_fan, fuel_air_ratio):
        PC = self.propulsion_module.get_PC()*1000
        outlet_speed_bar = self.compute_outlet_speed_bar(outlet_speed_hot_air, outlet_speed_fan, fuel_air_ratio)
        air_passage_ratio = self.get_rotation_air_passage_ratio(self.rotation)
        total_efficiency = (1 + air_passage_ratio) * (outlet_speed_bar - aircraft_speed) * aircraft_speed / (fuel_air_ratio * PC)
        return total_efficiency
    

def get_total_fuel_air_ratio(dict_fuel_air_ratio):
    list_stream_fuel_air_ratio = [dict_fuel_air_ratio[stream_k].values() for stream_k in dict_fuel_air_ratio]
    fuel_air_ratio_per_stream = [sum(stream_fuel_air_ratio) for stream_fuel_air_ratio in list_stream_fuel_air_ratio]

    total_fuel_air_ratio = sum(fuel_air_ratio_per_stream)

    return total_fuel_air_ratio

def get_list_outlet_speed(dict_outlet_speed):
    list_outlet_speed = [sum(i.values()) for i in dict_outlet_speed.values()]
    return list_outlet_speed