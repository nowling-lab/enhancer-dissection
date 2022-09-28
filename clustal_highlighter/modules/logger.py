from enum import Enum
import logging

workspace = None
checks = {}
warning_present = False
warnings = []

def print_error(print_str):
    warning_color = '\033[93m'
    end_color = '\033[0m'
    print(f'{warning_color}{print_str}{end_color}')
        
def print_ok(print_str):
    end_color = '\033[0m'
    success_color = '\033[92m'
    print(f'{success_color}{print_str}{end_color}')

def set_workspace(workspace_location:str):
    global workspace
    workspace = workspace_location
    
def add_check(self, check_name:str):
    return

def debug(logger:logging.Logger, message:str):
    logger.debug(message)

def info(logger:logging.Logger, message:str):
    logger.info(message)

def check_warnings():
    global warning_present
    global warnings
    if warning_present:
        print_error("Warnings present!")
        for warning in warnings:
            print_error(warning)
    else:
        print_ok("Runtime checks passed, check tmp.log for more details in your output directory")
    

def warning(logger:logging.Logger, message:str):
    global warning_present
    global warnings
    warning_present = True
    warnings.append(message)
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
            return (Status.OK, print_ok(f'{self.check_name} is OK. {data_string}'))
        else:
            return (Status.ERROR, print_error(f'{self.check_name} FAILED. {data_string}'))

def validate_reports(reports_generated, reports_requested):
    print(f'Total reports generated: {reports_generated}')
    print(f'Number of Reports Requested: {reports_requested}')
    if reports_generated != reports_requested:
        print_error('Numbers of reports requested not equal to reports outputted')
    else:
        print_ok('Correct number of reports generated')