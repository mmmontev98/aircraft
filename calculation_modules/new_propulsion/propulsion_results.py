import copy
from unittest import result

class PropulsionResults():
    list_of_efficiencies = ['thermal_efficiency', 'propulsion_efficiency', 'total_efficiency']
    list_of_performance = ['specific_thrust', 'TSFC', 'fuel_air_ratio']
    list_of_thermodynamic_states = ['T_0', 'P_0', 'outlet_speed']
    def __init__(self) -> None:
        self.dict_T_0 = {}
        self.dict_P_0 = {}
        self.dict_fuel_air_ratio = {}
        self.dict_outlet_speed = {}


    def set_T_0(self, T_0):
        self.T_0 = copy.deepcopy(T_0)
        
    def set_P_0(self, P_0):
        self.P_0 = copy.deepcopy(P_0)
        
    def set_fuel_air_ratio(self, fuel_air_ratio):
        self.fuel_air_ratio = copy.deepcopy(fuel_air_ratio)
        
    def set_outlet_speed(self, outlet_speed):
        self.outlet_speed = copy.deepcopy(outlet_speed)
        
    def set_specific_thrust(self, specific_thrust):
        self.specific_thrust = copy.deepcopy(specific_thrust)
        
    def set_TSFC(self, TSFC):
        self.TSFC = copy.deepcopy(TSFC)

    def set_thermal_efficiency(self, thermal_efficiency):
        self.thermal_efficiency = copy.deepcopy(thermal_efficiency)
        
    def set_propulsion_efficiency(self, propulsion_efficiency):
        self.propulsion_efficiency = copy.deepcopy(propulsion_efficiency)

    def set_total_efficiency(self, total_efficiency):
        self.total_efficiency = copy.deepcopy(total_efficiency)
    
    def get_T_0(self):
        return copy.deepcopy(self.T_0)
        
    def get_P_0(self):
        return copy.deepcopy(self.P_0)

    def get_fuel_air_ratio(self):
        return copy.deepcopy(self.fuel_air_ratio)

    def get_outlet_speed(self):
        return copy.deepcopy(self.outlet_speed)

    def get_specific_thrust(self):
        return copy.deepcopy(self.specific_thrust)

    def get_TSFC(self):
        return copy.deepcopy(self.TSFC)

    def get_thermal_efficiency(self):
        return copy.deepcopy(self.thermal_efficiency)

    def get_total_efficiency(self):
        return copy.deepcopy(self.total_efficiency)

    def get_propulsion_efficiency(self):
        return copy.deepcopy(self.propulsion_efficiency)

    def print_thermodynamic_states(self):
        print("-"*65)
        print("Thermodynamic States")
        print("-"*65)
        self.print_from_list(self.list_of_thermodynamic_states)
        print("-"*65)

    def print_efficiencies(self):
        print("-"*65)
        print("Propulsion Efficiencies")
        print("-"*65)
        self.print_from_list(self.list_of_efficiencies)
        print("-"*65)

    def print_performance(self):
        print("-"*65)
        print("Propulsion Performance")
        print("-"*65)
        self.print_from_list(self.list_of_performance)
        print("-"*65)
    
    def print_from_list(self, from_list):
        for parameter in from_list:
            result = getattr(self, 'get_' + parameter)()
            print(parameter, ': ', result)
    
    def print_all(self):
        self.print_thermodynamic_states()
        self.print_efficiencies()
        self.print_performance()

