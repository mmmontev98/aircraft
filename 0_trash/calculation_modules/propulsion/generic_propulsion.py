from abc import abstractclassmethod, ABC, abstractmethod
from .propulsion_parameters import PropulsionParameters
from physical_constants import PhysicalConstants

class GenericPropulsionSubmodule(ABC):
    def __init__(self, parameters: PropulsionParameters):
        self.parameters = parameters
    
    def initialize(self):
        self.mach = self.parameters.get_mach()
        self.pressure_a = self.parameters.get_pressure_a()
        self.temperature_a = self.parameters.get_temperature_a()
        self.aircraft_speed = self.parameters.get_aircraft_speed()

    def intake_process(self, T_a, P_a, mach, gamma_intake, eta_intake):
        T_02 = T_a*(1 + ((gamma_intake - 1)/2)*mach**2)
        exp = gamma_intake/(gamma_intake - 1)
        P_02 = P_a*(1 + eta_intake*(T_02/T_a -1))**(exp)
        
        return (T_02, P_02)
    
    def fan_process(self, T_02, P_02, fan_pressure_ratio, eta_fan, gamma_fan):
        P_08 = P_02*fan_pressure_ratio
        exp = (gamma_fan - 1)/gamma_fan
        T_08 = T_02*(1 + (1/eta_fan)*(fan_pressure_ratio**(exp)) - 1)
        
        return (T_08, P_08)

    def compressor_process(self, T_02, P_02, compressor_pressure_ratio, eta_compressor, gamma_compressor):
        P_03 = P_02*compressor_pressure_ratio
        exp = (gamma_compressor - 1)/gamma_compressor
        T_03 = T_02*(1 + (1/eta_compressor)*(compressor_pressure_ratio**(exp) - 1))
        
        return (T_03, P_03)

    def combustion_process(self, P_03, outlet_combustion_temperature, gamma_combustion, deltaP_0=0.0):
        P_04 = P_03 - deltaP_0
        T_04s = outlet_combustion_temperature
        exp = (gamma_combustion - 1)/gamma_combustion
        T_04 = T_04s * (P_04/P_03)**exp

        return (T_04, P_04)

    def combustion_f_process(self, T_04, T_03, PC, combustion_cp, eta_combustion):
        temperature_ratio = T_04/T_03
        f = (temperature_ratio - 1)/(eta_combustion*PC/(combustion_cp*T_03) - temperature_ratio)

        return f

    def turbine_compressor_process(self, T_04, P_04, gamma_turbine, eta_turbine, T_03, T_08):
        TET = T_04 - (T_03 - T_08)
        exp = gamma_turbine/(gamma_turbine - 1)
        PET = P_04*(1 - (1/eta_turbine)*(1 - TET/T_04))**exp

        return (TET, PET)

    def turbine_fan_process(self, TET, PET, B, gamma_turbine, eta_turbine, T_02, T_08):
        T_05 = TET - (B+1)(T_08 - T_02)
        exp = gamma_turbine/(gamma_turbine - 1)
        P_05 = PET*(1 - (1/eta_turbine)*(1 - T_05/TET))**exp

        return (T_05, P_05)

    def post_combustion_process(self, P_05, outlet_post_combustion_temperature):
        P_06 = P_05
        T_06 = outlet_post_combustion_temperature
        return (T_06, P_06)

    def post_combustion_f_process(self, T_06, T_05, PC, combustion_cp, eta_combustion):
        temperature_ratio = T_06/T_05
        f = (temperature_ratio - 1)/(eta_combustion*PC/(combustion_cp*T_05) - temperature_ratio)

        return f

    def nozzle_process(self, T_06, P_06):
        P_07 = P_06
        T_07 = T_06

        return T_07, P_07
    
    def fan_nozzle_process(self, T_08, P_08):
        P_09 = P_08
        T_09 = T_08

        return T_09, P_09
    
    def nozzle_u_process(self, T_06, P_06, P_s, eta_nozzle, gamma_nozzle, R):
        exp = (gamma_nozzle - 1)/gamma_nozzle
        u_s = (2*eta_nozzle*(1/exp)*R*T_06*(1 - (P_s/P_06)**exp))**(1/2)
        return u_s

    def fan_nozzle_u_process(self, T_08, P_08, P_s, eta_fan_nozzle, gamma_fan_nozzle, R):
        exp = (gamma_fan_nozzle - 1)/gamma_fan_nozzle
        u_s_fan = (2*eta_fan_nozzle*(1/exp)*R*T_08(1 - (P_s/P_08)**exp))**(1/2)
        return u_s_fan

    #1
    def correct_fan_pressure_ratio(self, fan_rotation, B_baseline):
        A = -0.00179*(B_baseline)**2 + 0.00687*(B_baseline) + 0.5
        C = 0.011*(B_baseline) + 0.53
        return  A*fan_rotation**2- 4.3317E-02*fan_rotation + C
    #2
    def correct_booster_pressure_ratio(self, fan_rotation):
        return 4.8967E-01*fan_rotation**2 - 4.3317E-02*fan_rotation + 5.6846E-01
    
    #3
    def correct_compressor_pressure_ratio(self, compressor_rotation):
        return -6.0730E+00*compressor_rotation**3 + 1.4821E+01*compressor_rotation**2- 1.0042E+01*compressor_rotation + 2.2915E+00

    
    #4
    def correct_outlet_combustion_temperature(self, compressor_rotation):
        return 8.1821E-01*compressor_rotation**2 - 2.2401E-01*compressor_rotation + 4.1842E-01

    #5
    def correct_fan_rotation(self, compressor_rotation):
        return 1.4166E+00*compressor_rotation - 4.0478E-01
    
    #6
    def correct_B(self, fan_rotation):
        return -8.3241E-01*fan_rotation**2 + 3.8824E-01*fan_rotation + 1.4263E+00
    
    #7
    def correct_eta_fan(self, fan_rotation):
        return -6.6663*fan_rotation**4 + 17.752*fan_rotation**3- 17.469*fan_rotation**2 + 7.7181*fan_rotation - 0.32985
    
    #8
    def correct_eta_compressor(self, compressor_rotation):
        return -1.1234E+00*compressor_rotation**2 + 2.1097E+00*compressor_rotation + 1.8617
    
    #9
    def correct_eta_turbine(self, rotation):
        return -6.7490E-02*rotation**2 + 2.5640E-01*rotation + 8.1153E-01
    
    #10
    def correct_eta_combustion(self, compressor_rotation):
        return 1.1630E+00*compressor_rotation**3 - 3.0851E+00*compressor_rotation**2 + 2.7312E+00*compressor_rotation + 1.9130E-01
    #11
    def correct_mass_flux(self, compressor_rotation):
        return  -6.6970E+00*compressor_rotation**3 + 1.7001E+01*compressor_rotation**2 - 1.2170E+01*compressor_rotation + 2.8717E+00



        

    
    @abstractclassmethod
    def compute_thermal_efficiency(self, f, PC, m_dot_a, u_s, u):
        '''kinetic_energy_power = m_dot_a*((1+f)*(u_s**2/2) - u**2/2)
        fuel_combustion_power = (f*PC)
        thermal_efficiency = kinetic_energy_power/fuel_combustion_power

        return thermal_efficiency'''
    
    @abstractclassmethod
    def compute_propulsion_efficiency(self, T, m_dot_a, f, u, u_s):
        '''propulsion_power = (T*u)
        kinetic_energy_power = m_dot_a*((1+f)*(u_s**2/2) - u**2/2)
        propulsion_efficiency = propulsion_power/kinetic_energy_power

        return propulsion_efficiency'''

    @abstractclassmethod
    def compute_total_efficiency(self):
        '''def total_efficiency(self, u_s, u, f, PC, turbofan_flag=False, B=0, u_bar_s=0):
        if turbofan_flag:
            total_efficiency = (1+B)*(u_bar_s - u)*u/(f*PC)
            return total_efficiency

        total_efficiency = (u_s - u)*u/(f*PC)
        return total_efficiency'''
    
    @abstractclassmethod
    def compute_specific_thrust(self):
        '''bla'''
    
    @abstractclassmethod
    def compute_TSFC(self):
        '''bla'''

    