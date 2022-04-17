from aircraft import Aircraft
from calculation_modules.new_propulsion.propulsion_wrapper import PropulsionWrapper

# ''' Propulsion Parameters'''
# efficiency = {
#     "eta_intake" : 0.97,
#     "eta_compressor" : 0.85,
#     "eta_combustion" : 1.0,
#     "eta_turbine" : 0.90,
#     "eta_nozzle" : 0.98 }
# specific_heat_ratio = {
#     "gamma_intake": 1.40, 
#     "gamma_compressor": 1.37, 
#     "gamma_combustion": 1.35, 
#     "gamma_turbine": 1.33, 
#     "gamma_nozzle": 1.36}
# combustor_cp = 1.11
# compressor_pressure_ratio = 30
# mean_R = 288.3
# outlet_combustion_temperature = 1600
# PCI = 45000

''' Analysis Parameters'''
mach = 0.85
Pa = 18.75*(10**3)
Ta = 216.7
N_2 = 1.00

''' Import Propulsion from file'''
# TurboJet21 = Aircraft('TurboJet21')
TurboJet21 = Aircraft('TurboFan22')
TurboJet21.load_aircraft()

new_propulsion_module = TurboJet21.get_new_propulsion_module()

# ''' Setting Propulsion manually'''
# turbojet = Aircraft()
# turbojet.change_aircraft_config('propulsion', 'TurboJet')
# propulsion_module = turbojet.get_propulsion_module()
# propulsion_module.set_efficiencies(efficiency)
# propulsion_module.set_combustor_cp(combustor_cp)
# propulsion_module.set_compressor_pressure_ratio(compressor_pressure_ratio)
# propulsion_module.set_mean_R(mean_R)
# propulsion_module.set_outlet_combustion_temperature(outlet_combustion_temperature)
# propulsion_module.set_PCI(PCI)
# propulsion_module.set_specific_heat_ratios(specific_heat_ratio)

''' Setting Computation Parameters'''
propulsion_wrapper = PropulsionWrapper(TurboJet21)
propulsion_wrapper.set_mach(mach)
propulsion_wrapper.set_pressure_a(Pa)
propulsion_wrapper.set_outlet_pressure(Pa)
propulsion_wrapper.set_temperature_a(Ta)
propulsion_wrapper.set_compressor_rotation(N_2)

''' Computing Results'''
propulsion_wrapper.initialize()
propulsion_wrapper.compute()
