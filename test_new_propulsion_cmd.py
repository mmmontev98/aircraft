from aircraft import Aircraft
from calculation_modules.new_propulsion.propulsion_wrapper import PropulsionWrapper

''' Aircraft definition'''
# aircraft_name = 'TurboJet21'
aircraft_name = 'TurboFan22'
# aircraft_name = 'RamJet21'

''' Import Propulsion from file'''
aircraft = Aircraft(aircraft_name)
aircraft.load_aircraft()

''' Analysis Parameters'''
mach = 0.85
Pa = 18.75#*(10**3)
Po = Pa
Ta = 216.7
N_2 = 0.8
rotation_flag=False

''' Setting Computation Parameters'''
propulsion_wrapper = PropulsionWrapper(aircraft)
propulsion_wrapper.set_mach(mach)
propulsion_wrapper.set_pressure_a(Pa)
propulsion_wrapper.set_outlet_pressure(Po)
propulsion_wrapper.set_temperature_a(Ta)
propulsion_wrapper.set_compressor_rotation(N_2)
propulsion_wrapper.set_rotation_flag(rotation_flag)

''' Computing Results'''
propulsion_wrapper.initialize()
propulsion_wrapper.compute()

propulsion_results = propulsion_wrapper.get_results()

propulsion_results.print_all()

# T_0 = propulsion_results.get_T_0()
# P_0 = propulsion_results.get_P_0()
# outlet_speed = propulsion_results.get_outlet_speed()
# fuel_air_ratio = propulsion_results.get_fuel_air_ratio()
# specific_thrust = propulsion_results.get_specific_thrust()
# TSFC = propulsion_results.get_TSFC()
# thermal_efficiency = propulsion_results.get_thermal_efficiency()
# total_efficiency = propulsion_results.get_total_efficiency()
# propulsion_efficiency = propulsion_results.get_propulsion_efficiency()

 