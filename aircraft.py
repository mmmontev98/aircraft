import os
import sys
import json
from copy import deepcopy

from aircraft_modules import Propulsion

class Aircraft():
    ''' Object that groups all the aircraft characteristics'''
    list_of_modules = ['new_propulsion']
    def __init__(self, aircraft_name='aircraft', dir_path=None, aircraft_config=None):
        # Default value (a dir_path ends with a '/')
        if dir_path is None:
            dir_path = os.getcwd()
        if dir_path[-1] != '/':
            dir_path += '/'
        self.dir_path = dir_path

        self.aircraft_name = aircraft_name

        # Creation of the different submodules, according to the aircraft_config dict provided
        if aircraft_config is None:
            aircraft_config = self.get_standard_aircraft_config()
        self.set_aircraft_config(aircraft_config)
    
    def get_dir_path(self):
        # Precaution
        if self.dir_path[-1] != '/':
            self.dir_path += '/'

        return self.dir_path

    def get_aircraft_name(self):
        return self.aircraft_name

    # =========================================================================== #
    # =============  FUNCTIONS HANDLING THE AIRCRAFT CONFIGURATION  ============== #
    # =========================================================================== #
    def get_standard_aircraft_config(self):
        aircraft_config = {}

        aircraft_config['new_propulsion'] = 'Propulsion'

        return aircraft_config

    def change_aircraft_config(self, module, module_name):
        """ Allows to change only one module type in the aircraft_config

        -------------------
        Args:
            module : the module you want to change : propulsion, geometry...
            module_name : the type you want (TurboJet, TurboFan...)
        """

        if module not in Aircraft.list_of_modules:
            print("[ERROR] This module is not possible. Choose among %s" % ', '.join(map(str, Aircraft.list_of_modules)))

        # Modification of the aircraft_config
        self.aircraft_config[module] = module_name
        self.create_module(module, module_name)
    
    def set_aircraft_config(self, aircraft_config):
        self.aircraft_config = aircraft_config

        for module in Aircraft.list_of_modules:
            if hasattr(self, module):
                if aircraft_config[module] != getattr(self, module + '_module').get_module_name():
                    self.create_module(module, aircraft_config[module])
            else:
                self.create_module(module, aircraft_config[module])
    
    def get_aircraft_config(self):
        return deepcopy(self.aircraft_config)

    # =========================================================================== #
    # ===================  FUNCTIONS FOR THE AIRCRAFT MODULES  =================== #
    # =========================================================================== #
    def create_module(self, module, module_name):
        """ Just a wrapping function for each individual module creation """
        getattr(self, 'create_' + module + '_module')(module_name)
    
    def create_new_propulsion_module(self, module_name):
        self.new_propulsion_module = Propulsion()

    def get_new_propulsion_module(self):
        return self.new_propulsion_module

    # =========================================================================== #
    # ==========================  SAVE & LOAD FUNCTIONS  ======================== #
    # =========================================================================== #
    def get_aircraft_dict(self, simplified_version=False):
        aircraft_dict = {}
        pass

    def save_aircraft(self):
        """ 
        It saves the aircraft
        """
        pass

    def load_aircraft(self, special_name=None):
        load_dir_path = './database/aircraft/' + self.aircraft_name + '/'

        with open(load_dir_path + 'aircraft.json', 'r') as file:
            aircraft_dict = json.load(file)

        # Loading from the big dictionary
        aircraft_information = aircraft_dict['aircraft_information']

        module_information = aircraft_dict['module_information']

        # Create the adequate set of module
        for module in Aircraft.list_of_modules:
            self.change_aircraft_config(module, aircraft_information[module])
            
            module_dict = getattr(self, module + '_module').get_module_dictionary(module_information[module])

            getattr(self, module + '_module').load_module(module_dict)
