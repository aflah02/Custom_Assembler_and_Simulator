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
            
def isLabelValid(line_comp,alphanum):
    a = line_comp[0]
    counter = 0
    b = len(a) - 1
    if a[-1::] = ":":
        for i in a:
            if i in aplhanum:
                counter+=1
        if counter == b:
            
                
        else:
            return -1 
        
def isLineValid(line_comp):
    """Checks if line is valid that is the instruction is valid and the size corresponds to the instruction"""
    if isInstructionValid(line_comp[0]) == False:
        return -1
    if isSizeRight(line_comp[0], line_comp) == False:
        return -2
    else:
        return 1


def lineTypesMatch(line_comp):
    """Checks if the objects in the line match the objects which they were supposed to be i.e. registers
    are in place of registers in the syntax and so on"""
    ls_type_order = type_to_syntaxconstituents[OPcode_table[line_comp[0]][-1]]
    for i in range(1, len(line_comp)):
        if ls_type_order[i] == 'Register':
            if isRegisterValid(line_comp[i]) is False:
                return -1
            if isRegisterValid(line_comp[i])==-1:
                return -4
        if ls_type_order[i] == 'Immediate':
            if isImmediateValid(line_comp[i]) is False:
                return -2
            if isImmediateRangeValid(line_comp[i]) is False:
                return -3
        if ls_type_order[i] == 'Memory Address':
            if line_comp[0]=='ld' or line_comp[0]=='st':
                if line_comp[-1] in var_declared:
            if line_comp[0]=='jmp' or line_comp[0]=='jlt' or line_comp[0]=='jgt' or line_comp[0]=='je': 
                if line_comp[-1] in lbl_declared:
                else
            else:
                return -5
    return 0
