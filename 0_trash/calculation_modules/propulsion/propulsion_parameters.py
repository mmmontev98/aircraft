class PropulsionParameters():
    def __init__(self, aircraft_module=None):
        self.aircraft_module = aircraft_module
    
    def set_aircraft_module(self, aircraft_module):
        self.aircraft_module = aircraft_module
    
    def set_mach(self, mach):
        self.mach = mach
    
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

    def get_aircraft_module(self):
        return self.aircraft_module
    
    def get_propulsion_module(self):
        return self.aircraft_module.get_propulsion_module()
    
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
        gamma_intake = self.get_propulsion_module().get_specific_heat_ratios()['gamma_intake']
        R_mean = self.get_propulsion_module().get_mean_R()
        aircraft_speed = self.mach * (self.temperature_a * gamma_intake * R_mean)**(1/2)
        return aircraft_speed
    