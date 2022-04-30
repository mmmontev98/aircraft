from aircraft_modules.propulsion.propulsion import Propulsion
from .generic_propulsion import GenericPropulsionSubmodule
from ..propulsion_parameters import PropulsionParameters

class TurboPropCompute(GenericPropulsionSubmodule):
    def __init__(self, parameters: PropulsionParameters):
        super().__init__(parameters)
        self.parameters = parameters
        self.propulsion_module : Propulsion = parameters.get_aircraft_module().get_propulsion_module()

    
    def compute(self):
        dict_outlet_speed, dict_fuel_air_ratio = self.compute_thermodynamic_states()
        
        self.compute_performance_parameters(dict_outlet_speed, dict_fuel_air_ratio)

        
    
    def compute_performance_parameters(self, dict_outlet_speed, dict_fuel_air_ratio):

        aircraft_speed = self.parameters.get_aircraft_speed()
        list_outlet_speed = get_list_outlet_speed(dict_outlet_speed)
        total_fuel_air_ratio = get_total_fuel_air_ratio(dict_fuel_air_ratio)
        
        outlet_speed = list_outlet_speed[0]

        specific_power_turbine = self.compute_specific_power_turbine(total_fuel_air_ratio)
        specific_thrust = self.compute_specific_thrust(aircraft_speed, outlet_speed, total_fuel_air_ratio)
        TSFC = self.compute_TSFC(aircraft_speed, outlet_speed, total_fuel_air_ratio)
        BSFC = self.compute_BSFC(total_fuel_air_ratio)
        EBSFC = self.compute_EBSFC(aircraft_speed, outlet_speed, total_fuel_air_ratio)
        
        thermal_efficiency = self.compute_thermal_efficiency(aircraft_speed, outlet_speed, total_fuel_air_ratio)
        propulsion_efficiency = self.compute_propulsion_efficiency(aircraft_speed, outlet_speed, total_fuel_air_ratio)
        total_efficiency = self.compute_total_efficiency(aircraft_speed, outlet_speed, total_fuel_air_ratio)
        
        turbine_power = self.compute_power_turbine(total_fuel_air_ratio)
        propeller_thrust = self.compute_thrust_propeller(aircraft_speed, total_fuel_air_ratio)
        thrust_nozzle = self.compute_hot_air_thrust(aircraft_speed, outlet_speed, total_fuel_air_ratio)
        thrust_total = self.compute_thrust_total(aircraft_speed, outlet_speed, total_fuel_air_ratio)
        fuel_consumption = self.compute_fuel_consumption(aircraft_speed, outlet_speed, total_fuel_air_ratio)

        
        self.results.set_specific_power_turbine(specific_power_turbine)
        self.results.set_specific_thrust(specific_thrust)
        
        self.results.set_BSFC(BSFC)
        self.results.set_TSFC(TSFC)
        self.results.set_EBSFC(EBSFC)
        
        self.results.set_thermal_efficiency(thermal_efficiency)
        self.results.set_propulsion_efficiency(propulsion_efficiency)
        self.results.set_total_efficiency(total_efficiency)
        
        self.results.set_nozzle_thrust(thrust_nozzle)
        self.results.set_propeller_thrust(propeller_thrust)
        self.results.set_thrust(thrust_total)
        self.results.set_turbine_power(turbine_power)
        self.results.set_fuel_consumption(fuel_consumption)
        
    def compute_hot_air_thrust(self, aircraft_speed, outlet_speed, fuel_air_ratio):
        if self.parameters.get_mass_flow() is not None:
            rotation = self.parameters.get_compressor_rotation()
            specific_thrust = self.compute_specific_thrust(aircraft_speed, outlet_speed, fuel_air_ratio)
            mass_flow = self.get_rotation_mass_flow(rotation)
            thrust = specific_thrust * mass_flow
            return thrust
        
        return None
    
    def compute_thrust_propeller(self, aircraft_speed, fuel_air_ratio):
        propeller_efficiency = self.propulsion_module.get_propeller_efficiency()
        propeller_power = self.compute_power_propeller(fuel_air_ratio)
        if aircraft_speed > 0:
            thrust_propeller = propeller_power*propeller_efficiency / aircraft_speed
        else:
            thrust_propeller = 0

        return thrust_propeller

    def compute_thrust_total(self, aircraft_speed, outlet_speed, fuel_air_ratio):
        if self.parameters.get_mass_flow() is not None:
            thrust_propeller = self.compute_thrust_propeller(aircraft_speed, fuel_air_ratio)
            hot_air_thrust = self.compute_hot_air_thrust(aircraft_speed, outlet_speed, fuel_air_ratio)
            return thrust_propeller + hot_air_thrust
        
        return None

        

    def compute_power_propeller(self, fuel_air_ratio):
        power_turbine = self.compute_power_turbine(fuel_air_ratio)
        gearbox_power_ratio = self.propulsion_module.get_gearbox_power_ratio()

        propeller_power = power_turbine*gearbox_power_ratio

        return propeller_power
        
    
    def compute_power_turbine(self, fuel_air_ratio):
        if self.parameters.get_mass_flow() is not None:
            rotation = self.parameters.get_compressor_rotation()
            mass_flow = self.get_rotation_mass_flow(rotation)
            specific_power_turbine = self.compute_specific_power_turbine(fuel_air_ratio)
            power_turbine = specific_power_turbine * mass_flow
            return power_turbine
        
        return None

    def compute_fuel_consumption(self, aircraft_speed, outlet_speed, fuel_air_ratio):
        if self.parameters.get_mass_flow() is not None:
            thrust_turbine = self.compute_power_turbine(fuel_air_ratio)
            EBSFC = self.compute_EBSFC(aircraft_speed, outlet_speed, fuel_air_ratio)
            fuel_consumption = thrust_turbine * EBSFC
            return fuel_consumption
        
        return None
        

    def compute_specific_thrust(self, aircraft_speed, outlet_speed, fuel_air_ratio):
        specific_thrust = (1 + fuel_air_ratio)*outlet_speed - aircraft_speed
        return specific_thrust/1000

    def compute_specific_power_turbine(self, fuel_air_ratio):
        turbine_free = self.process_streams.get_component(1,'turbine_free')
        specific_work = turbine_free.get_specific_work()
        specific_power_turbine = (specific_work)*(1 + fuel_air_ratio)

        return specific_power_turbine

    def compute_TSFC(self, aircraft_speed, outlet_speed, fuel_air_ratio):
        if self.parameters.get_mass_flow() is not None:
            rotation = self.parameters.get_compressor_rotation()
            mass_flow = self.get_rotation_mass_flow(rotation)
            thrust_hot_air = self.compute_hot_air_thrust(aircraft_speed, outlet_speed, fuel_air_ratio)
            propeller_thrust = self.compute_thrust_propeller(aircraft_speed, fuel_air_ratio)
            TSFC = fuel_air_ratio*mass_flow/(thrust_hot_air+propeller_thrust)
            return TSFC
        return None
    
    def compute_BSFC(self, fuel_air_ratio):
        specific_power_turbine = self.compute_specific_power_turbine(fuel_air_ratio)
        BSFC = fuel_air_ratio/specific_power_turbine
        return BSFC
    
    def compute_EBSFC(self, aircraft_speed, outlet_speed, fuel_air_ratio):
        specific_thrust = self.compute_specific_thrust(aircraft_speed, outlet_speed, fuel_air_ratio)
        specific_power_thrust = specific_thrust * aircraft_speed
        specific_power_turbine = self.compute_specific_power_turbine(fuel_air_ratio)
        EBSFC = fuel_air_ratio/(specific_power_thrust + specific_power_turbine)
        return EBSFC

    def compute_thermal_efficiency(self, aircraft_speed, outlet_speed, fuel_air_ratio):
        PC = self.propulsion_module.get_PC()*1000
        kinetic_energy_power = (1+fuel_air_ratio)*(outlet_speed**2/2) - aircraft_speed**2/2
        fuel_combustion_power = fuel_air_ratio*PC
        thermal_efficiency = kinetic_energy_power/fuel_combustion_power

        return thermal_efficiency
    
    def compute_propulsion_efficiency(self, aircraft_speed, outlet_speed, fuel_air_ratio):
        specific_thrust = self.compute_specific_thrust(aircraft_speed, outlet_speed, fuel_air_ratio)
        propulsion_power = (specific_thrust*aircraft_speed)
        kinetic_energy_power = (1+fuel_air_ratio)*(outlet_speed**2/2) - aircraft_speed**2/2
        propulsion_efficiency = propulsion_power/kinetic_energy_power

        return propulsion_efficiency

    def compute_total_efficiency(self, aircraft_speed, outlet_speed, fuel_air_ratio):
        PC = self.propulsion_module.get_PC()*1000
        total_efficiency = (outlet_speed - aircraft_speed)*aircraft_speed/(fuel_air_ratio*PC)
        return total_efficiency


def get_total_fuel_air_ratio(dict_fuel_air_ratio):
    list_stream_fuel_air_ratio = [dict_fuel_air_ratio[stream_k].values() for stream_k in dict_fuel_air_ratio]
    fuel_air_ratio_per_stream = [sum(stream_fuel_air_ratio) for stream_fuel_air_ratio in list_stream_fuel_air_ratio]

    total_fuel_air_ratio = sum(fuel_air_ratio_per_stream)

    return total_fuel_air_ratio

def get_list_outlet_speed(dict_outlet_speed):
    list_outlet_speed = [sum(i.values()) for i in dict_outlet_speed.values()]
    return list_outlet_speed