import subprocess
import json
import re
import os
import time
import logging
import argparse
import sys

from typing import List
from agent import Agent
from abc import ABC, abstractmethod
from communication_mediator import CommunicationMediator
from message import Message

from agent_labels import label

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# TODO: 
#   1. Maybe use SHELL = FALSE
#   2. Sanitize LLM output


@label("agent", "mensab")
class MensabAgent(Agent):

    def __init__(self, comm_mediator: CommunicationMediator):
        self.comm_mediator = comm_mediator
        self.id = self.__class__._labels[1]  

    def get_id(self):
        return self.id

    def log(self, level: str, message: str):
        level = level.lower()  
        getattr(logging, level)(message)  

    def send_request(self, model_name: str, messages: List[str]):
        payload = {
            "model": model_name,
            "stream": False,
            "messages": [{"role": "user", "content": msg} for msg in messages]
        }

        result = subprocess.run(
            ["curl", "-s", "http://localhost:11434/api/chat", "-d", json.dumps(payload)],
            capture_output=True, text=True
        )

        return json.loads(result.stdout)

    def start_model(self, model_name: str):
        self.log("INFO", f"Running model: {model_name}")
        
        subprocess.Popen("ollama serve", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
        # Temporary
        time.sleep(2)

        result = subprocess.run("ollama list", capture_output=True, text=True, shell=True)
        output = result.stdout
        
        if model_name not in output:
            self.log("ERROR", "Model is not available among those already downloaded")
            # Don't need an exit 
            sys.exit(1)

    def run(self, model_name: str):
        self.start_model(model_name)

        while True:
            self.log("INFO",  "LLM agent waiting for a message")
            user_input = self.comm_mediator.get_response(receiver = self.id)[0]
            user_input = user_input["body"]

            if "sleep" in user_input.lower():
                self.log("INFO", "Shutting down llm agent...")
                message = Message(sender = self.id, receiver = "s2t", body = "sleep")
                self.comm_mediator.handle_request(message)
                subprocess.run(f"ollama stop {model_name}", shell=True)
                break

            # Check host OS with command
            response = self.send_request(model_name, [
                "You are on MacOs. The user will give you some task. In order to execute these tasks you must write some BASH script. Do not add comments or further explanations about the code or how to use it. If its not possible to write BASH code just say so, without adding anything else. Be correct and concise.",
                user_input
            ])

            response_content = response.get("message", {}).get("content", "")

            script_path = os.path.expanduser("~/temp_script.sh")
                
            with open(script_path, "w") as script_file:
                script_file.write("#!/bin/bash\n")
                script_file.write(response_content)
                
            os.chmod(script_path, 0o755)
            result = subprocess.run([script_path], capture_output=True, text=True, stdin=subprocess.DEVNULL)

            if result.returncode != 0:
                error = result.stderr

                full_response = self.send_request(
                    model_name,
                    [
                        "You are on MacOs. The user will provide you an error related to an execution of a bash script, with the relative code. The user is not technical, so don't adopt a technical language. Your explanations about the error should be as intuitive as possible.",
                        error
                    ]
                )
                    
                model_response = full_response.get("message", {}).get("content", "")
                self.log("INFO", f"Mensab: {model_response}")
            else:
                self.log("INFO", "Script eseguito correttamente.")


            os.remove(script_path)

            message = Message(sender = self.id, receiver = "s2t", body = "OK")
            self.comm_mediator.handle_request(message)
            self.log("INFO", "LLM agent sent a response")

