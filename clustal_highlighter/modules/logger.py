from enum import Enum
import logging

workspace = None
checks = {}

def set_workspace(workspace_location:str):
    global workspace
    workspace = workspace_location
    
def add_check(self, check_name:str):
    return

def debug(logger:logging.Logger, message:str):
    logger.debug(message)

def info(logger:logging.Logger, message:str):
    logger.info(message)

def warning(logger:logging.Logger, message:str):
    logger.warning(message)

def error(logger:logging.Logger, message:str):
    logger.error(message)
        
class Status(Enum):
    OK = True 
    ERROR = False
        
class check:
    def __init__(self, check_name: str, description: str,  gathered, outputted):
        self.check_name = check_name
        self.description = description
        self.gathered = gathered
        self.outputted = outputted
        
    def run_check(self):
        data_string = f'{self.description} gathered: {self.gathered}. {self.description} ouputted: {self.outputted}'
        
        if(self.gathered == self.outputted):
            return (Status.OK, generate_ok(f'{self.check_name} is OK. {data_string}'))
        else:
            return (Status.ERROR, generate_error(f'{self.check_name} FAILED. {data_string}'))
        
        
def generate_error(print_str):
    warning_color = '\033[93m'
    end_color = '\033[0m'
    return f'{warning_color}{print_str}{end_color}'
        
def generate_ok(print_str):
    end_color = '\033[0m'
    success_color = '\033[92m'
    return f'{success_color}{print_str}{end_color}'
