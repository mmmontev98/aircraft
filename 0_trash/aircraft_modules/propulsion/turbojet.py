from .generic_propulsion import GenericPropulsion

class TurboJet(GenericPropulsion):
    def __init__(self):
        self.efficiencies = {}
        self.specific_heat_ratios = {}
        self.efficiencies['eta_intake'] = 0.95
        self.efficiencies['eta_compressor'] = 0.85
        self.efficiencies['eta_combustion'] = 0.99
        self.efficiencies['eta_turbine'] = 0.90
        self.efficiencies['eta_nozzle'] = 0.95
        self.specific_heat_ratios['gamma_intake'] = 1.40
        self.specific_heat_ratios['gamma_compressor'] = 1.40
        self.specific_heat_ratios['gamma_combustion'] = 1.40
        self.specific_heat_ratios['gamma_turbine'] = 1.40
        self.specific_heat_ratios['gamma_nozzle'] = 1.40
    
    def initialize(self):
        pass

    def set_efficiencies(self, efficiency):
        self.efficiencies = efficiency
        
    def set_specific_heat_ratios(self, specific_heat_ratio):
        self.specific_heat_ratios = specific_heat_ratio

    def set_compressor_pressure_ratio(self, compressor_pressure_ratio):
        self.compressor_pressure_ratio = compressor_pressure_ratio

    def set_outlet_combustion_temperature(self, outlet_combustion_temperature):
        self.outlet_combustion_temperature = outlet_combustion_temperature

    def set_PCI(self, PCI):
        self.PCI = PCI

    def set_mean_R(self, mean_R):
        self.mean_R = mean_R

    def set_combustor_cp(self, combustor_cp):
        self.combustor_cp = combustor_cp

    def get_efficiencies(self):
        return self.efficiencies

    def get_specific_heat_ratios(self):
        return self.specific_heat_ratios
    
    def get_compressor_pressure_ratio(self):
        return self.compressor_pressure_ratio

    def get_outlet_combustion_temperature(self):
        return self.outlet_combustion_temperature

    def get_PCI(self):
        return self.PCI

    def get_mean_R(self):
        return self.mean_R

    def get_combustor_cp(self):
        return self.combustor_cp


    def load_module(self, module_dict):
        self.set_efficiencies(module_dict['efficiencies'])
        self.set_specific_heat_ratios(module_dict['specific_heat_ratios'])
        self.set_compressor_pressure_ratio(module_dict['compressor_pressure_ratio'])
        self.set_outlet_combustion_temperature(module_dict['outlet_combustion_temperature'])
        self.set_PCI(module_dict['PCI'])
        self.set_mean_R(module_dict['mean_R'])
        self.set_combustor_cp(module_dict['combustor_cp'])