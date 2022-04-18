import numpy as np
import matplotlib.pyplot as plt
from aircraft import Aircraft
from aircraft_modules import new_propulsion
from aircraft_modules.new_propulsion.components import component_stream
from calculation_modules.new_propulsion.propulsion_wrapper import PropulsionWrapper

def main():
    ''' Component Parameters'''
    aircraft_name = 'TurboJet21'

    ''' Analysis Parameters'''
    list_of_mach = [0, 0.85, 2.00]
    list_of_Pa = [101.30, 18.75, 7.170]
    list_of_Ta = [288.2, 216.7, 216.7]
    N_2 = 1
    list_of_pressure_ratio = np.linspace(5, 100, 40)
    list_of_combustor_outlet_temperature = [1300, 1500, 1700]
    rotation_flag = False

    aircraft = load_aircraft(aircraft_name)
    new_propulsion_module = aircraft.get_new_propulsion_module()
    
    compressor = new_propulsion_module.get_component(1, 'compressor')
    combustor = new_propulsion_module.get_component(1, 'combustor')

    fig1 = plt.figure(figsize=(1,3))
    fig1.suptitle("specific_thrust")
    
    fig2 = plt.figure()
    fig2.suptitle("list_of_TSFC")
    
    fig3 = plt.figure()
    fig3.suptitle("list_of_thermal_efficiency")
    for k, (mach, Pa, Ta) in enumerate(zip(list_of_mach, list_of_Pa, list_of_Ta)):
        axis1 = fig1.add_subplot(1,3,k+1)
        axis2 = fig2.add_subplot(1,3,k+1)
        axis3 = fig3.add_subplot(1,3,k+1)
        Po = Pa

        for combustor_outlet_temperature in list_of_combustor_outlet_temperature:
            combustor.set_outlet_temperature(combustor_outlet_temperature)
            list_of_TSFC = []
            list_of_specific_thrust = []
            list_of_thermal_efficiency = []
            list_of_propulsion_efficiency = []
            for pressure_ratio in list_of_pressure_ratio:
                compressor.set_pressure_ratio(pressure_ratio)
                propulsion_wrapper = set_propulsion_parameters(aircraft, mach, Pa, Po, Ta, N_2, rotation_flag)
                propulsion_wrapper.initialize()
                propulsion_wrapper.compute()
                propulsion_results = propulsion_wrapper.get_results()
                
                list_of_TSFC.append(propulsion_results.get_TSFC())
                list_of_specific_thrust.append(propulsion_results.get_specific_thrust())
                list_of_thermal_efficiency.append(propulsion_results.get_thermal_efficiency())
                list_of_propulsion_efficiency.append(propulsion_results.get_propulsion_efficiency())

            
            
            axis1.plot(list_of_pressure_ratio, list_of_specific_thrust, marker='o', label = combustor_outlet_temperature)
            axis1.set_ylim([0, 1200])
            axis1.set_title("m = {}, T_a = {}, P_a = {}".format(mach, Ta, Pa))
            axis1.legend()

            
            axis2.plot(list_of_pressure_ratio, list_of_TSFC, marker='o', label = combustor_outlet_temperature)
            axis2.set_ylim([0, 0.00006])
            axis2.set_title("m = {}, T_a = {}, P_a = {}".format(mach, Ta, Pa))
            axis2.legend()
            
            axis3.plot(list_of_pressure_ratio, list_of_thermal_efficiency, marker='o', label = combustor_outlet_temperature)
            axis3.set_ylim([0, 0.7])
            axis3.set_title("m = {}, T_a = {}, P_a = {}".format(mach, Ta, Pa))
            axis3.legend()


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
    