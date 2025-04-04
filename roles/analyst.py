import os
import copy
import json
import argparse
import tqdm
import time


from core import interface
from utils import code_truncate, construct_system_message
from roles.prompts import get_ds1000_analyzer_prompt


class Analyst(object):
    def __init__(self, TEAM, ANALYST, requirement, model='gemini-2.0-flash', majority=1, max_tokens=512,
                                temperature=0.0, top_p=1.0):
        self.model = model
        self.majority = majority
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.history_message = []
        self.requirement=requirement
        self.itf = interface.ProgramInterface(
            stop='',
            verbose=False,
            model = self.model,
        )

        system_message = construct_system_message(requirement, ANALYST, TEAM)
        self.history_message_append(system_message)


    def analyze(self):
        analyst_prompt=get_ds1000_analyzer_prompt(self.requirement)
        try:
            responses = self.itf.run(prompt=analyst_prompt, majority_at = self.majority, max_tokens=self.max_tokens, temperature=self.temperature, top_p=self.top_p)
        except Exception as e:
            print(e)
            print("analyze fail")
            time.sleep(5)
            return "error"

        plan = responses[0]
        self.history_message_append(plan, "assistant")
    
        return analyst_prompt,plan
    
    def history_message_append(self, system_message, role="user"):
        self.history_message.append({
            "role": role,
            "parts": [system_message]
        })


