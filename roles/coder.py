import os
import openai
import time
import copy
import json
import argparse
import tqdm

from core import interface
from utils import code_truncate, construct_system_message
from roles.instruction import INSTRUCTPLAN, INSTRUCTREPORT, INSTRUCTCODE
from roles.prompts import get_ds1000_generator_prompt

class Coder(object):
    def __init__(self, TEAM, PYTHON_DEVELOPER, requirement, model='gemini-2.0-flash', majority=1, max_tokens=512,
                                temperature=0.0, top_p=1.0):
        self.model = model
        self.majority = majority
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.history_message = []
        self.requirement = requirement

        self.itf = interface.ProgramInterface(
            stop='',
            verbose=False,
            model = self.model,
        )

        system_message = construct_system_message(requirement, PYTHON_DEVELOPER, TEAM)

        self.history_message_append(system_message)

    def implement(self, report, is_init=False):
        self.construct_with_report(report, is_init)
        #print(self.history_message)
        generator_prompt=get_ds1000_generator_prompt(self.requirement,report)      
        try:
            responses = self.itf.run(prompt=generator_prompt, majority_at = self.majority, max_tokens=self.max_tokens, temperature=self.temperature, top_p=self.top_p)
        except Exception as e:
            print(e)
            print("implement fail")
            time.sleep(5)
            return generator_prompt,"error"
             
        # HumanEval Style
        # if 'gpt' not in self.model:
        #     generation = responses[0][responses[0].find("def"):]
        #     tem = [s for s in generation.split('\n\n') if 'def ' in s or s[:1] == ' ']
        #     code = '\n\n'.join(tem).strip('```').strip()
        # else:
        #     code = code_truncate(responses[0])

        # DS-1000 Style
        code=responses[0]      
        self.history_message = self.history_message[:-1]
        self.history_message_append(code, "assistant")
    
        return generator_prompt,code
    
    def history_message_append(self, system_message, role="user"):
        self.history_message.append({
            "role": role,
            "parts": [system_message]
        })
        
    def construct_with_report(self, report, is_init=False):
        if report != "":
            if is_init:
                instruction = INSTRUCTPLAN.format(report=report.strip())
            else:
                instruction = INSTRUCTREPORT.format(report=report.strip())
            self.history_message_append(instruction)
            self.history_message_append(INSTRUCTCODE.format(requirement=self.requirement))
