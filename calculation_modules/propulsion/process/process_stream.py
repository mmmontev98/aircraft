import sys

from aircraft_modules.propulsion.components import GenericPropulsionComponent
from aircraft_modules.propulsion.components import ComponentStream
from aircraft_modules.propulsion.components import Booster, Combustor, Compressor, Fan
from aircraft_modules.propulsion.components import Intake, Nozzle, PostCombustor, Turbine

from .generic_propulsion_process import GenericPropulsionProcess
from . import IntakeProcess, CompressionProcess, CombustionProcess, ExpansionProcess, NozzleProcess


class ProcessStream():
    def __init__(self, parameters):
        self.process_streams = {}
        self.parameters = parameters
    
    def set_component_stream(self, component_streams: ComponentStream):
        self.component_streams = component_streams

    def initialize(self):
        component_stream_dict = self.component_streams.get_streams()
        for component_stream_id in component_stream_dict:
            if component_stream_id not in self.process_streams:
                self.process_streams[component_stream_id] = {}
            for component_name in component_stream_dict[component_stream_id]:
                component = component_stream_dict[component_stream_id][component_name]
                process = self.create_component_process(component)
                self.process_streams[component_stream_id][component_name] = process
        
        self.link_components()
    
    def link_components(self):
        component_stream_dict = self.component_streams.get_streams()
        for stream_id in self.process_streams:
            for component_name in self.process_streams[stream_id]:
                component = component_stream_dict[stream_id][component_name]
                linked_component = component.get_linked_component()
                if component.get_linked_component():
                    process = self.process_streams[stream_id][component_name]
                    linked_process = self.process_streams[stream_id][linked_component]
                    process.set_linked_component_process(linked_process)


    def create_component_process(self, component) -> GenericPropulsionProcess:
        if isinstance(component, Intake):
            process_module = IntakeProcess(self.parameters, component)
        elif isinstance(component, (Combustor, PostCombustor)):
            process_module = CombustionProcess(self.parameters, component)
        elif isinstance(component, (Compressor, Fan, Booster)):
            process_module = CompressionProcess(self.parameters, component)
        elif isinstance(component, Turbine):
            process_module = ExpansionProcess(self.parameters, component)        
        elif isinstance(component, Nozzle):
            process_module = NozzleProcess(self.parameters, component)
        else:
            print("[ERROR] No such component, %s, version exists for Propulsion()" % component.__class__.__name__)
            sys.exit()
        
        return process_module
    
    def get_number_of_streams(self):
        return len(self.streams)
    
    def get_streams(self) -> dict[str: [GenericPropulsionComponent]]:
        return self.process_streams
    
    def get_component(self, stream_id, component_name):
        return self.process_streams[stream_id][component_name]

    def compute_stream(self, T_a, P_a):
        dict_T_0 = {}
        dict_P_0 = {}
        dict_fuel_air_ratio = {}  
        dict_outlet_speed = {}

        for stream in self.process_streams:
            temperature = T_a
            pressure = P_a 
            for component_name in self.process_streams[stream]:
                process = self.process_streams[stream][component_name]
                
                (temperature, pressure) = process.get_thermodynamic_state(temperature, pressure)
                set_thermodynamic_states(dict_T_0, component_name, temperature, stream)
                set_thermodynamic_states(dict_P_0, component_name, pressure, stream)
                
                if isinstance(process, CombustionProcess):
                    fuel_air_ratio = process.get_fuel_air_ratio()
                    set_thermodynamic_states(dict_fuel_air_ratio, component_name, fuel_air_ratio, stream)
                
                if isinstance(process, NozzleProcess):
                    outlet_speed = process.get_outlet_speed(temperature, pressure)
                    set_thermodynamic_states(dict_outlet_speed, component_name, outlet_speed, stream)
        
        return dict_T_0, dict_P_0, dict_outlet_speed, dict_fuel_air_ratio


def set_thermodynamic_states(dict_thermodynamic_state, component_name, thermodynamic_state, stream_id):
    if stream_id not in dict_thermodynamic_state:
        dict_thermodynamic_state[stream_id] = {}
    dict_thermodynamic_state[stream_id][component_name] = thermodynamic_state