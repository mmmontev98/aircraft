from .generic_propulsion import GenericPropulsionSubmodule
from .propulsion_parameters import PropulsionParameters

class TurboJetCompute(GenericPropulsionSubmodule):
    def __init__(self, parameters: PropulsionParameters):
        super().__init__(parameters)
        self.parameters = parameters
        self.post_combustion_flag = False

    def initialize(self):
        pass
        
    def compute(self):
        T_a = self.parameters.get_temperature_a()
        P_a = self.parameters.get_pressure_a()
        P_s = self.parameters.get_outlet_pressure()
        mach = self.parameters.get_mach()
        compressor_rotation = self.parameters.get_compressor_rotation()
        aircraft_speed = self.parameters.get_aircraft_speed()
        propulsion_module = self.parameters.get_propulsion_module()
        efficiencies = propulsion_module.get_efficiencies()
        gammas = propulsion_module.get_specific_heat_ratios()
        T_0 = {}
        P_0 = {}

        #intake process
        eta_intake = efficiencies['eta_intake']
        (T_0['2'], P_0['2']) = self.intake_process(T_a, P_a, mach, gammas['gamma_intake'], eta_intake)
        
        # compressor 
        eta_compressor = efficiencies['eta_compressor'] * self.correct_eta_compressor(compressor_rotation)
        compressor_pressure_ratio = propulsion_module.get_compressor_pressure_ratio() * self.correct_compressor_pressure_ratio(compressor_rotation)
        (T_0['3'], P_0['3']) = self.compressor_process(T_0['2'], P_0['2'], compressor_pressure_ratio,  eta_compressor, gammas['gamma_compressor'])
        
        # combustion process
        outlet_combustion_temperature = propulsion_module.get_outlet_combustion_temperature() * self.correct_outlet_combustion_temperature(compressor_rotation)
        combustor_PCI = propulsion_module.get_PCI()
        combustor_cp = propulsion_module.get_combustor_cp()
        eta_combustion = efficiencies['eta_combustion'] * self.correct_eta_combustion(compressor_rotation)
        (T_0['4'], P_0['4']) = self.combustion_process(P_0['3'], outlet_combustion_temperature, gammas['gamma_combustion'])
        fuel_air_ratio = self.combustion_f_process(T_0['4'], T_0['3'], combustor_PCI, combustor_cp, eta_combustion)

        # turbine process
        eta_turbine = efficiencies['eta_turbine'] * self.correct_eta_turbine(compressor_rotation)
        (T_0['5'], P_0['5']) = self.turbine_compressor_process(T_0['4'], P_0['4'], gammas['gamma_turbine'], eta_turbine, T_0['3'], T_0['2'])

        # post_combustion
        if self.post_combustion_flag:
            eta_post_combustion = efficiencies['eta_combustion']
            (T_0['6'], P_0['6']) = self.post_combustion_process(P_0['5'], outlet_combustion_temperature)
            fuel_air_ratio_post_combustion = self.post_combustion_f_process(T_0['6'],T_0['5'], combustor_PCI, combustor_cp, eta_post_combustion)
            fuel_air_ratio = fuel_air_ratio + fuel_air_ratio_post_combustion
        else:
            (T_0['6'], P_0['6']) = (T_0['5'], P_0['5'])
        
        # nozzle process
        R_mean = propulsion_module.get_mean_R()
        eta_nozzle = efficiencies['eta_nozzle']
        outlet_speed = self.nozzle_u_process(T_0['6'], P_0['6'], P_s, eta_nozzle, gammas['gamma_nozzle'], R_mean)
        (T_0['7'], P_0['7']) = self.nozzle_process(T_0['6'], P_0['6'])

        specific_thrust = self.compute_specific_thrust(aircraft_speed, outlet_speed, fuel_air_ratio) / self.correct_mass_flux(compressor_rotation)
        TSFC = self.compute_TSFC(aircraft_speed, outlet_speed, fuel_air_ratio) * self.correct_mass_flux(compressor_rotation)

    
        return T_0, P_0, specific_thrust, TSFC

    
    def compute_specific_thrust(self, aircraft_speed, outlet_speed, fuel_air_ratio):
        specific_thrust = (1 + fuel_air_ratio)*outlet_speed - aircraft_speed
        return specific_thrust

    def compute_TSFC(self, aircraft_speed, outlet_speed, fuel_air_ratio):
        specific_thrust = self.compute_specific_thrust(aircraft_speed, outlet_speed, fuel_air_ratio)
        TSFC = fuel_air_ratio/specific_thrust
        return TSFC

    def compute_thermal_efficiency(self, fuel_air_ratio, PC, outlet_speed, aircraft_speed):
        kinetic_energy_power = (1+fuel_air_ratio)*((outlet_speed**2)/2) -( aircraft_speed**2)/2
        fuel_combustion_power = fuel_air_ratio*PC
        thermal_efficiency = kinetic_energy_power/fuel_combustion_power

        return thermal_efficiency
    
    
    def compute_propulsion_efficiency(self, specific_thrust, fuel_air_ratio, aircraft_speed, outlet_speed):
        propulsion_power = (specific_thrust*aircraft_speed)
        kinetic_energy_power = (1+fuel_air_ratio)*(outlet_speed**2/2) - aircraft_speed**2/2
        propulsion_efficiency = propulsion_power/kinetic_energy_power

        return propulsion_efficiency

    def compute_total_efficiency(self, fuel_air_ratio, PC, outlet_speed, aircraft_speed):
        total_efficiency = (outlet_speed - aircraft_speed)*aircraft_speed/(fuel_air_ratio*PC)
        return total_efficiency
        
