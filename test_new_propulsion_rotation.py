import numpy as np
import matplotlib.pyplot as plt
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
    Pa = 101.63
    Po = Pa
    Ta = 290
    list_of_N_2 = np.linspace(0.5, 1.0, 20)
    list_of_air_passage_ratio = np.linspace(4, 12, 20)
    rotation_flag = True
    list_of_results = []
    list_of_TSFC = []
    list_of_specific_thrust = []
    list_of_thermal_efficiency = []
    list_of_propulsion_efficiency = []

    aircraft = load_aircraft(aircraft_name)
    new_propulsion_module = aircraft.get_new_propulsion_module()

    

    for air_passage_ratio in list_of_air_passage_ratio:
        new_propulsion_module.set_air_passage_ratio(air_passage_ratio)
        propulsion_wrapper = set_propulsion_parameters(aircraft, mach, Pa, Po, Ta, N_2, rotation_flag)
        propulsion_wrapper.initialize()
        propulsion_wrapper.compute()
        propulsion_results = propulsion_wrapper.get_results()
        
        list_of_results.append(propulsion_results)
        
        list_of_TSFC.append(propulsion_results.get_TSFC())
        list_of_specific_thrust.append(propulsion_results.get_specific_thrust())
        list_of_thermal_efficiency.append(propulsion_results.get_thermal_efficiency())
        list_of_propulsion_efficiency.append(propulsion_results.get_propulsion_efficiency())


    for N_2 in list_of_N_2:
        propulsion_wrapper = set_propulsion_parameters(aircraft, mach, Pa, Po, Ta, N_2, rotation_flag)
        propulsion_wrapper.initialize()
        propulsion_wrapper.compute()
        propulsion_results = propulsion_wrapper.get_results()
        
        list_of_results.append(propulsion_results)
        
        list_of_TSFC.append(propulsion_results.get_TSFC())
        list_of_specific_thrust.append(propulsion_results.get_specific_thrust())
        list_of_thermal_efficiency.append(propulsion_results.get_thermal_efficiency())
        list_of_propulsion_efficiency.append(propulsion_results.get_propulsion_efficiency())

    fig = plt.figure()
    axis = fig.add_subplot(111)
    axis.plot(list_of_N_2, list_of_specific_thrust, marker='o')
    axis.set_title("specific_thrust")

    fig = plt.figure()
    axis = fig.add_subplot(111)
    axis.plot(list_of_N_2, list_of_TSFC, marker='o')
    axis.set_title("list_of_TSFC")

    fig = plt.figure()
    axis = fig.add_subplot(111)
    axis.plot(list_of_N_2, list_of_thermal_efficiency, marker='o')
    axis.set_title("list_of_thermal_efficiency")


    plt.show(block=False)

    input('\n Type enter to end')




    



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


if __name__ == '__main__':
    main()
    