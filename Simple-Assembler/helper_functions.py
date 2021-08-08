from general_consts import *
from register_and_type_constants import *
from validity_checker import *

def getRegisterEncoding(register):
    """Returns Register Encoding"""
    return register_to_encoding[register]


def getRegisterCount(type):
    """Returns Register Count"""
    return type_to_reg_no[type]


def isLineValid(line):
    """Checks if line is valid that is the instruction is valid and the size corresponds to the instruction"""
    ls_input = list(map(str, line.split()))
    if isInstructionValid(ls_input[0]) == False:
        return -1
    if isSizeRight(ls_input[0], ls_input) == False:
        return -2
    else:
        return 1


def lineTypesMatch(line):
    """Checks if the objects in the line match the objects which they were supposed to be i.e. registers
    are in place of registers in the syntax and so on"""
    ls_input = list(map(str, line.split()))
    valid = True
    ls_type_order = type_to_syntaxconstituents[OPcode_table[ls_input[0]][-1]]
    for i in range(1, len(ls_input)):
        if ls_type_order[i] == 'Register':
            if isRegisterValid(ls_input[i]) is False:
                valid = False
                break
        elif ls_type_order[i] == 'Immediate':
            if isImmediateValid(ls_input[i]) is False:
                valid = False
                break
        else:
            pass
    return valid