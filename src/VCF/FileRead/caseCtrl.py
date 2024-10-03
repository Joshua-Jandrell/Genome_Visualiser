"""
Contains classes and functions to read and interpret case and control files
"""
from typing import Literal
from Util.boolStr import str_to_bool, is_bool
CASE_KEY = ['case', 'case:']
CTRL_KEY = ['ctrl', 'ctrl:', 'control', 'control:']

class EmptyFileError(ValueError):
    pass


def read_case_ctrl(case_path:str)->tuple[list[str],list[str]]:




    cases = []
    ctrls = []
    if case_path != '':
        with open(case_path, mode='r') as f:
            lines = f.read().split('\n')

            if len(lines) == 0:
                raise EmptyFileError(f"The file {case_path} is empty")

            # Check to see if a bool-list format is used 
            if len(lines[0].split()) == 1:
                cases = lines
            else:
                cases = [line.split()[1] for line in lines if is_bool(line.split()[1]) and str_to_bool(line.split()[1])]
                ctrls = [line.split()[1] for line in lines if is_bool(line.split()[1]) and not str_to_bool(line.split()[1])]
            f.close()


    return cases, ctrls
