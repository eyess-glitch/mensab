import threading
from communication_mediator import CommunicationMediator
from llm_agent import MensabAgent
from s2t_agent import SpeechToTextAgent

def main():
    comm_mediator = CommunicationMediator()
    
    mensab = MensabAgent(comm_mediator)
    s2t_agent = SpeechToTextAgent(comm_mediator)
    
    mensab_thread = threading.Thread(target=partial(mensab.run, "qwen2.5-coder:7b"))
    s2t_thread = threading.Thread(target=s2t_agent.run)
    
    s2t_thread.start()
    mensab_thread.start()
    
    mensab_thread.join()
    s2t_thread.join()

if __name__ == "__main__":
    main()