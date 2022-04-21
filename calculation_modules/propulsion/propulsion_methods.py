from .propulsion_parameters import PropulsionParameters

class SetFunctions():
    def __init__(self, parameters: PropulsionParameters):
        self.parameters = parameters
    
    def set_aircraft_module(self, aircraft_module):
        self.parameters.set_aircraft_module(aircraft_module)
    
    def set_mach(self, mach):
        self.parameters.set_mach(mach)
    
    def set_pressure_a(self, pressure_a):
        self.parameters.set_pressure_a(pressure_a)
    
    def set_outlet_pressure(self, outlet_pressure):
        self.parameters.set_outlet_pressure(outlet_pressure)

    def set_temperature_a(self, temperature_a):
        self.parameters.set_temperature_a(temperature_a)

    def set_compressor_rotation(self, compressor_rotation):
        self.parameters.set_compressor_rotation(compressor_rotation)

    def set_mass_flow(self, mass_flow):
        self.parameters.set_mass_flow(mass_flow)

    def set_rotation_flag(self, rotation_flag):
        self.parameters.set_rotation_flag(rotation_flag)
