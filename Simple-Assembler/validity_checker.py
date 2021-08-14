from general_consts import *
from register_and_type_constants import *
from OPcode_table import *

def isInstructionValid(instruction):
    """Checks if instruction is valid"""
    if instruction in ls_instructions:
        return True
    else:
        return False

def isInstructionValid2(instruction):
    """Checks if instruction is valid"""
    if instruction in ls_instructions2:
        return True
    else:
        return False
    
def isRegisterValid(register):
    """Checks if register is valid"""
    if register in ls_registers:
        if register == 'FLAGS':
            return -1
        else:
            return True
    else:
        return False


def isImmediateValid(immediate):
    """Checks if immediate is valid"""
    if immediate[0] != '$':
        return False
    else:
        return True

def isImmediateRangeValid(immediate):
    if int(immediate[1:]) >= 0 and int(immediate[1:]) <= 255:
        return True
    else:
        return False

def isSizeRight(instruction, ls):
    """Checks if required number of arguments are there or not"""
    type_instruction = OPcode_table[instruction][-1]
    if instruction=='mov':
        if len(ls)==3:
            return True
    if len(ls) == type_to_input_len[type_instruction]:
        return True
    return False
