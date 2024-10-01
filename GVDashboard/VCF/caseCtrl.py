"""
Contains classes and functions to manage case and control files
"""
import os
from typing import Literal, Iterable

from numpy import ndarray

CASE_KEY = ['case', 'case:']
CTRL_KEY = ['ctrl', 'ctrl:', 'control', 'control:']

def read_case_ctrl(case_path:str|None, ctrl_path:str|None)->tuple[list[str],list[str]]:

    if case_path == '':
        case_path = None
    if ctrl_path == "":
        ctrl_path = None

    if case_path == ctrl_path:
        ctrl_path = None

    cases = []
    ctrls = []
    if case_path is not None:
        with open(case_path, mode='r') as f:
            lines = f.read().split('\n')
            cases = lines
            f.close()

            # if len(lines[0].split())>=2:
            #     for l in lines:
            #         cases.append(l.split()[0])
            #         ctrls.append(l.split()[1])
            #     return cases, ctrls
            # else:
            #     cases = lines
    if ctrl_path is not None and case_path != ctrl_path:
        with open(ctrl_path, mode='r') as f:
            lines = f.read().split('\n')
            ctlrs = lines
            f.close()

    return cases, ctrls


    


            
class CaseCtrlSet():
    def __init__(self,file_path:str):
        mode:Literal['none', 'case', 'ctrl'] = 'case'
        self._case_list=[]
        self._ctrl_list=[]
        with open(file_path) as f:
            line = f.readline().split()
            for sample in line:
                if sample in CASE_KEY: mode = 'case'
                elif sample in CTRL_KEY: mode = "ctrl"
                elif mode == 'case': self._case_list.append(sample)
                elif mode == 'ctrl': self._ctrl_list.append(sample)
    #def is_case(self):

    # def get_cases(self,data:ndarray,samples:Iterable):
    #     case_mask = [sample]
