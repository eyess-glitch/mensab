from abc import ABC, abstractmethod

class Agent(ABC):
    
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def get_id(self):
        pass

