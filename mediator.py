from abc import ABC, abstractmethod

class Mediator(ABC):
    
    @abstractmethod
    def handle_request(self, message):
        pass

    @abstractmethod
    def get_response(self):
        pass

