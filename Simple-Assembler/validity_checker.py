from general_consts import *
from register_and_type_constants import *


def isInstructionValid(instruction):
    """Checks if instruction is valid"""
    if instruction in ls_instructions:
        return True
    else:
        return False


def isRegisterValid(register):
    """Checks if register is valid"""
    if register in ls_registers:
        return True
    else:
        return False


def isImmediateValid(immediate):
    """Checks if instruction is valid"""
    if immediate >= 0 and immediate <= 255:
        return True
    else:
        return False


def getRegisterEncoding(register):
    """Returns Register Encoding"""
    return register_to_encoding[register]


def getRegisterCount(type):
    """Returns Register Count"""
    return type_to_reg_no[type]