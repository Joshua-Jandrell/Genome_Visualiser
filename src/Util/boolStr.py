"""
Contains functions used to evaluate string and convert them to bool values.
"""
TRUE_STRS = ['true', 'yes', 'one', 'on', '1']
FALSE_STRS = ['false', 'no', 'zero', 'off', '0']

def is_bool(s:str)->bool:
    """
    Returns `True` if the given string represents a boolean value.\n
    """
    return s.lower() in TRUE_STRS + FALSE_STRS

def str_to_bool(s:str)->bool:
    """
    Convert a `str` type object to a `bool` type object based on its contents.
    This function accepts a wider range of values then the default python constructor.\n
    > Empty strings are evaluated as `False`.
    > Incompressable strings are evaluated as `True`.
    """
    if s.strip().lower() in FALSE_STRS+['']: return False
    return True
    
