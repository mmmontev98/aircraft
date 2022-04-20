from abc import ABC, abstractclassmethod

class GenericPropulsionProcess(ABC):
    def __init__(self):
        # self.component_module = component
        # self.parameters = parameters
        # self.rotation_flag = parameters.get_rotation_flag()
        self.linked_component_process = None
    
    @abstractclassmethod
    def get_thermodynamic_state(self):
        '''Returns the thermodynamic state after going through the component process'''

    def get_component_name(self):
        return self.component_module.get_name()
    
    def set_linked_component_process(self, linked_component_process):
        self.linked_component_process = linked_component_process
    
    def get_linked_component_process(self):
        return self.linked_component_process
    
    def get_baseline_efficiency(self):
        return self.component_module.get_efficiency()

    def get_rotation_efficiency(self, rotation):
        
        baseline_efficiency = self.get_baseline_efficiency()
        if not self.rotation_flag:
            return baseline_efficiency

        return self.component_module.get_rotation_efficiency(rotation)

