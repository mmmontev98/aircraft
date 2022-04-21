from aircraft_modules.propulsion.components.fan import Fan
from aircraft_modules.propulsion.generic_propulsion import GenericPropulsion
from aircraft_modules.propulsion.propulsion import Propulsion

class PropulsionParameters():
    def __init__(self, aircraft_module=None):
        self.aircraft_module = aircraft_module
        self.rotation_flag = True
        self.mass_flow = None
        self.polynomial_rotation_mass_flow = [-6.6970E+00, 1.7001E+01, -1.2170E+01, 2.8717E+00]
    
    def set_aircraft_module(self, aircraft_module):
        self.aircraft_module = aircraft_module
    
    def set_mach(self, mach):
        self.mach = mach
    
    def set_mass_flow(self, mass_flow):
        self.mass_flow = mass_flow
    
    def set_pressure_a(self, pressure_a):
        self.pressure_a = pressure_a
    
    def set_outlet_pressure(self, outlet_pressure):
        self.outlet_pressure = outlet_pressure

    def set_temperature_a(self, temperature_a):
        self.temperature_a = temperature_a

    def set_altitude(self, altitude):
        self.altitude = altitude

    def set_compressor_rotation(self, rotation):
        self.rotation = rotation

    def set_rotation_flag(self, rotation_flag):
        self.rotation_flag = rotation_flag
    
    def set_polynomial_rotation_mass_flow(self, polynomial_rotation_mass_flow):
        self.polynomial_rotation_mass_flow = polynomial_rotation_mass_flow
    
    def get_polynomial_rotation_mass_flow(self):
        return self.polynomial_rotation_mass_flow
    
    def get_rotation_flag(self):
        return self.rotation_flag

    def get_aircraft_module(self):
        return self.aircraft_module

    def get_mass_flow(self):
        return self.mass_flow
    
    def get_propulsion_module(self) -> Propulsion:
        return self.aircraft_module.get_propulsion_module()

    def get_fan_module(self) -> Fan:
        return self.get_propulsion_module().get_fan_module()
    
    def get_propulsion_module_string(self):
        return self.aircraft_module.get_aircraft_config()['propulsion']

    
    def get_mach(self):
        return self.mach
    
    def get_pressure_a(self):
        return self.pressure_a
    
    def get_outlet_pressure(self):
        return self.outlet_pressure

    def get_temperature_a(self):
        return self.temperature_a

    def get_compressor_rotation(self):
        return self.rotation


    def get_aircraft_speed(self):
        gamma_intake = self.get_propulsion_module().get_specific_heat_ratio_a()
        R_mean = self.get_propulsion_module().get_mean_R()
        aircraft_speed = self.mach * (self.temperature_a * gamma_intake * R_mean)**(1/2)
        return aircraft_speed