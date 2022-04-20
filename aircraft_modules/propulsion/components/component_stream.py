from .generic_propulsion_component import GenericPropulsionComponent

class ComponentStream():
    def __init__(self):
        self.streams = {}
        self.component_module_list = []
    
    def set_component_stream(self, component, stream_id):
        if isinstance(stream_id, list):
            for each_stream in stream_id:
                self.set_component_stream(component, each_stream)
        else:
            if stream_id not in self.streams:
                self.streams[stream_id] = {}
            
            component_name = component.get_name()
            self.streams[stream_id][component_name] = component

    def add_component(self, component: GenericPropulsionComponent):
        component_stream_id = component.get_stream_id()
        self.set_component_stream(component, component_stream_id)
        self.component_module_list.append(component)
    
    def get_number_of_streams(self):
        return len(self.streams)

    def get_component(self, stream_id, component_name):
        return self.streams[stream_id][component_name]
    
    def get_streams(self) -> dict[str: [GenericPropulsionComponent]]:
        return self.streams