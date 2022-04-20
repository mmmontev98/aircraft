from aircraft import Aircraft
from aircraft_modules.propulsion.components.nozzle import Nozzle
from calculation_modules.propulsion.propulsion_wrapper import PropulsionWrapper


''' Analysis Parameters'''
mach = 0.85
Pa = 18.75#*(10**3)
Po = Pa
Ta = 216.7
N_2 = 0.8
rotation_flag=False

''' Propulsion systems global parameters'''
aircraft_module_config = "propulsion"
aircraft_module_information = "TurboFan"
number_of_streams = 2
air_passage_ratio = 5
mean_R = 288.3
specific_heat_ratio_a = 1.40
cp = 1.11
PC = 45000

''' Dictionary of components information '''
components_dict = {
"intake":{
    "type": "intake",
    "stream_id": [1,2],
    "efficiency": 0.97,
    "specific_heat_ratio": 1.40,
    "polynomial_rotation_efficiency": [1]
},
"fan":{
    "type": "fan",
    "stream_id": [1, 2],
    "efficiency": 0.85,
    "specific_heat_ratio": 1.40,
    "pressure_ratio": 1.5,
    "air_passage_ratio": 5,
    "polynomial_rotation_fan_compressor": [1],
    "polynomial_rotation_efficiency": [1],
    "polynomial_rotation_pressure_ratio": [[1], [1], [1]],
    "polynomial_rotation_air_passage_ratio": [1]
},
"compressor":{
    "type": "compressor",
    "stream_id": 1,
    "efficiency": 0.85,
    "specific_heat_ratio": 1.37,
    "pressure_ratio": 20,
    "air_passage_ratio": 0,
    "polynomial_rotation_efficiency": [1],
    "polynomial_rotation_pressure_ratio": [1]
},
"combustor":{
    "type": "combustor",
    "stream_id": 1,
    "efficiency": 1.0,
    "specific_heat_ratio": 1.35,
    "outlet_temperature": 1600,
    "cp": 1.11,
    "PCI": 45000,
    "polynomial_rotation_efficiency": [1],
    "polynomial_rotation_outlet_temperature": [1]
},
"turbine_compressor":{
    "type": "turbine",
    "stream_id": 1,
    "efficiency": 0.90,
    "specific_heat_ratio": 1.33,
    "polynomial_rotation_efficiency": [1],
    "linked_component": "compressor"
},
"turbine_fan":{
    "type": "turbine",
    "stream_id": 1,
    "efficiency": 0.90,
    "specific_heat_ratio": 1.33,
    "polynomial_rotation_efficiency": [1],
    "linked_component": "fan"
},
"nozzle_hot_air":{
    "type": "nozzle",
    "stream_id": 1,
    "efficiency": 0.98,
    "specific_heat_ratio": 1.36,
    "mean_R": 288.3,
    "polynomial_rotation_efficiency": [1]
},
"nozzle_fan":{
    "type": "nozzle",
    "stream_id": 2,
    "efficiency": 0.98,
    "specific_heat_ratio": 1.40,
    "mean_R": 288.3,
    "polynomial_rotation_efficiency": [1]
}
}


nozzle_fan_type = "nozzle"
nozzle_fan_stream_id = 2
nozzle_fan_efficiency = 0.98
nozzle_fan_specific_heat_ratio = 1.40
nozzle_fan_mean_R = 288.3
nozzle_fan_name = "nozzle_fan"
polynomial_rotation_efficiency = [1]


''' Defining aircraft'''
aircraft = Aircraft()
aircraft.change_aircraft_config(aircraft_module_config, aircraft_module_information)
propulsion_module = aircraft.get_propulsion_module()

'''Defining Propulsion Module'''
propulsion_module.set_air_passage_ratio(air_passage_ratio)
propulsion_module.set_mean_R(mean_R)
propulsion_module.set_specific_heat_ratio_a(specific_heat_ratio_a)
propulsion_module.set_cp(cp)
propulsion_module.set_PC(PC)
propulsion_module.set_components(components_dict)

'''' Defining a component individually'''
nozzle_fan = Nozzle()
nozzle_fan.set_type(nozzle_fan_type)
nozzle_fan.set_stream_id(nozzle_fan_stream_id)
nozzle_fan.set_efficiency(nozzle_fan_efficiency)
nozzle_fan.set_specific_heat_ratio(nozzle_fan_specific_heat_ratio)
nozzle_fan.set_mean_R(nozzle_fan_mean_R)
nozzle_fan.set_name(nozzle_fan_name)
nozzle_fan.set_polynomial_rotation_efficiency(polynomial_rotation_efficiency)

''' Adding a new component to the propulsion module'''
propulsion_module.add_component(nozzle_fan)


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


T_0 = propulsion_wrapper.get_results().get_T_0()
P_0 = propulsion_wrapper.get_results().get_P_0()
outlet_speed = propulsion_wrapper.get_results().get_outlet_speed()
fuel_air_ratio = propulsion_wrapper.get_results().get_fuel_air_ratio()
specific_thrust = propulsion_wrapper.get_results().get_specific_thrust()
TSFC = propulsion_wrapper.get_results().get_TSFC()
thermal_efficiency = propulsion_wrapper.get_results().get_thermal_efficiency()
total_efficiency = propulsion_wrapper.get_results().get_total_efficiency()
propulsion_efficiency = propulsion_wrapper.get_results().get_propulsion_efficiency()

print('T_0: ', '\n', T_0, '\n')
print('P_0: ', '\n', P_0, '\n')
print('outlet_speed: ', outlet_speed, '\n')
print('fuel_air_ratio: ', fuel_air_ratio, '\n')
print('specific_thrust: ', specific_thrust, '\n')
print('TSFC: ', TSFC, '\n')
print('thermal_efficiency: ', thermal_efficiency, '\n')
print('propulsion_efficiency: ', propulsion_efficiency, '\n')
print('total_efficiency: ', total_efficiency, '\n')

 