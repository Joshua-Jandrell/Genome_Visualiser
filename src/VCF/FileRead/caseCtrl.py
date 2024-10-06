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
    print("ccc here")
    cases = []
    ctrls = []
    if case_path != '':
        with open(case_path, mode='r') as f:
            lines = f.read().split('\n')

            if len(lines) == 0:
                raise EmptyFileError(f"The file {case_path} is empty")
            
            split_str = " "
            if case_path[-4:] == ".csv":
                split_str = ","

                print(lines[0].split(split_str))

            # Check to see if a bool-list format is used 
            if len(lines[0].split(split_str)) == 1:
                cases = lines
            else:
                # Filter out empty line
                lines = [line for line in lines if len(line.split(split_str)) >= 2]
                cases = [line.split(split_str)[0] for line in lines if is_bool(line.split(split_str)[1]) and str_to_bool(line.split(split_str)[1])]
                ctrls = [line.split(split_str)[0] for line in lines if is_bool(line.split(split_str)[1]) and not str_to_bool(line.split(split_str)[1])]
                print(cases)
                print(ctrls)

            f.close()



    return cases, ctrls
