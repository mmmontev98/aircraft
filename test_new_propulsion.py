from aircraft import Aircraft
from calculation_modules.new_propulsion.propulsion_wrapper import PropulsionWrapper

def main():
    ''' Component Parameters'''
    # aircraft_name = 'TurboJet21'
    aircraft_name = 'TurboFan23'
    # aircraft_name = 'TurboFan22'
    # aircraft_name = 'RamJet21'

    ''' Analysis Parameters'''
    mach = 0
    # mach = 0.85
    # Pa = 18.75
    Pa = 101.63
    Po = Pa
    # Ta = 216.7
    Ta = 290
    N_2 = 1.0
    rotation_flag=False

    aircraft = load_aircraft(aircraft_name)
    propulsion_wrapper = set_propulsion_parameters(aircraft, mach, Pa, Po, Ta, N_2, rotation_flag)
    propulsion_wrapper.initialize()
    propulsion_wrapper.compute()

    propulsion_results = propulsion_wrapper.get_results()

    propulsion_results.print_all()
    

def load_aircraft(aircraft_name):
    ''' Import Propulsion from file'''
    aircraft = Aircraft(aircraft_name)
    aircraft.load_aircraft()

    return aircraft

def set_propulsion_parameters(aircraft, mach, Pa, Po, Ta, N_2, rotation_flag=True):
    ''' Setting Computation Parameters'''
    propulsion_wrapper = PropulsionWrapper(aircraft)
    propulsion_wrapper.set_mach(mach)
    propulsion_wrapper.set_pressure_a(Pa)
    propulsion_wrapper.set_outlet_pressure(Po)
    propulsion_wrapper.set_temperature_a(Ta)
    propulsion_wrapper.set_compressor_rotation(N_2)
    propulsion_wrapper.set_rotation_flag(rotation_flag)
    return propulsion_wrapper    

def get_results(propulsion_wrapper):
    T_0 = propulsion_wrapper.get_results().get_T_0()
    P_0 = propulsion_wrapper.get_results().get_P_0()
    outlet_speed = propulsion_wrapper.get_results().get_outlet_speed()
    fuel_air_ratio = propulsion_wrapper.get_results().get_fuel_air_ratio()
    specific_thrust = propulsion_wrapper.get_results().get_specific_thrust()
    TSFC = propulsion_wrapper.get_results().get_TSFC()
    thermal_efficiency = propulsion_wrapper.get_results().get_thermal_efficiency()
    total_efficiency = propulsion_wrapper.get_results().get_total_efficiency()
    propulsion_efficiency = propulsion_wrapper.get_results().get_propulsion_efficiency()

    return T_0

if __name__ == '__main__':
    main()
    