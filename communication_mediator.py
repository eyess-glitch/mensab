from mediator import Mediator
import threading
import queue
from message import Message
from agent_labels import get_classes


class CommunicationMediator(Mediator):
    def __init__(self):
        self.message_queue = {}
        agents = get_classes("agent")

        for agent in agents:
            agent_id = agent._labels[1]   
            self.message_queue[agent_id] = queue.Queue()
        
    def handle_request(self, message: Message):
        sender = message.get_("sender")
        receiver = message.get_("receiver")
        body = message.get_("body")
        self.message_queue[receiver].put({"sender": sender, "body": body})
            
    def get_response(self, receiver: str):
        receiver_queue = self.message_queue[receiver]        

        messages = []
        messages.append(receiver_queue.get())
        
        try:
            while True:
                messages.append(receiver_queue.get(block=False))
        except queue.Empty:
            pass
        
        return messages