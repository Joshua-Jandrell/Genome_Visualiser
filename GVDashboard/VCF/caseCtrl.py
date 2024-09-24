"""
Contains classes and functions to manage case and control files
"""
import os
from typing import Literal, Iterable

from numpy import ndarray

CASE_KEY = ['case', 'case:']
CTRL_KEY = ['ctrl', 'ctrl:', 'control', 'control:']
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
