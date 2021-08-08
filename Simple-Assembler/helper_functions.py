from general_consts import *
from register_and_type_constants import *
from validity_checker import *

def getRegisterEncoding(register):
    """Returns Register Encoding"""
    return register_to_encoding[register]


def getRegisterCount(type):
    """Returns Register Count"""
    return type_to_reg_no[type]

def isValid(line):
    ls_input = list(map(str, line.split()))
    if isInstructionValid(ls_input[0]) is False:
        return -1
    else:
        pass