from general_consts import *
from register_and_type_constants import *
from validity_checker import *

def getRegisterEncoding(register):
    """Returns Register Encoding"""
    return register_to_encoding[register]


def getRegisterCount(type):
    """Returns Register Count"""
    return type_to_reg_no[type]

def isVarValid(line_comp, count, alphanum):
    a = line_comp[1]
    b = len(a)
    counter = 0
    if line_comp[0]=='var':
        if count!=1:
            return -1
        else:
            for i in a:
                if i in alphanum:
                    counter+=1
            if counter==b:
                return -2
            else:
                return -3
            

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
    ls_type_order = type_to_syntaxconstituents[OPcode_table[ls_input[0]][-1]]
    for i in range(1, len(ls_input)):
        if ls_type_order[i] == 'Register':
            if isRegisterValid(ls_input[i]) is False:
                return -1
            if isRegisterValid(ls_input[i])==-1:
                return -4
        elif ls_type_order[i] == 'Immediate':
            if isImmediateValid(ls_input[i]) is False:
                return -2
            if isImmediateRangeValid(ls_input[i]) is False:
                return -3
        else:
            pass
    return 0
