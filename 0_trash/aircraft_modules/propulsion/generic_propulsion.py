from abc import abstractclassmethod
from ..generic_module import generic_module

class GenericPropulsion(generic_module):
    @abstractclassmethod
    def initialize(self):
        '''initialize the module'''
    
    @abstractclassmethod
    def get_efficiencies() -> dict:
        """ Returns the efficiency of each proccess
        ======================
        efficiencies is a dictionary with:
        keys: the corresponding process
        values: the corresponding efficiency to the process

        -------------------
        Returns:
            efficiencies: dict
        """

    @abstractclassmethod
    def get_specific_heat_ratios() -> dict:
        """ Returns the specific heat ratio of each proccess
        ======================
        specific_heat_ratios is a dictionary with:
        keys: the corresponding process
        values: the corresponding specific heat ratio to the process

        -------------------
        Returns:
            specific_heat_ratios: dict
        """

    @abstractclassmethod
    def get_compressor_pressure_ratio() -> float:
        """ Returns the compressor pressure ratio
        ======================
        compressor_pressure_ratio is the pressure ratio of the given compressor
        -------------------
        Returns:
            compressor_pressure_ratio: float
        """
    
    @abstractclassmethod
    def get_outlet_combustion_temperature() -> float:
        """ Returns the outlet combustion temperature
        ======================
        outlet_combustion_temperature is the given temperature in the outlet of the combustion chamber
        -------------------
        Returns:
            outlet_combustion_temperature: float
        """

    @abstractclassmethod
    def get_PCI() -> float:
        """ Returns the PCI of the fuel
        ======================
        PCI of the fuel
        -------------------
        Returns:
            PCI: float
        """
    
    @abstractclassmethod
    def get_mean_R() -> float:
        """ Returns the mean R of the propulsion
        ======================
        mean_R is the mean constant R of all the process of the propulsion
        -------------------
        Returns:
            mean_R: float
        """
    
    @abstractclassmethod
    def get_combustor_cp() -> float:
        """ Returns the specific heat of the fuel
        ======================
        combustor_cp is the given specific heat of the fuel
        -------------------
        Returns:
            combustor_cp: float
        """