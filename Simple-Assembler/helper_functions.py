from general_consts import *
from register_and_type_constants import *
from validity_checker import *

def getRegisterEncoding(register):
    """Returns Register Encoding"""
    return register_to_encoding[register]


def getRegisterCount(type):
    """Returns Register Count"""
    return type_to_reg_no[type]

def isVarValid(var_declared,var_called,alphanum,inst):
    inst2 = inst.copy()
    inst2.append('var')
    for i in var_declared:
        if i[1]!=1:
            return -1
        if i[1]==1:
            a = i[0]
            b = len(a)
            count = 0
            for i in a:
                if i in alphanum:
                    count+=1
            if count!=b:
                return -2
    count2 = 0
    b2 = len(var_called)
    var2 = []
    for i in var_declared:
        var2.append(i[0])
    for i in var2:
        if i in inst2:
            return -4
    for i in var_called:
        if i in var2:
            count2+=1
    if count2!=b2:
        return -3 
    return 0 #no issues all variables declared and called are valid

def isLabelValid(lbl_called,lbl_declared,lbl_inst,inst,alphanum): #add in main
    inst2 = inst.copy()
    inst2.append('var')
    for i in lbl_declared:
        count2 = 0
        a = i[0]
        b = len(a)
        count = 0
        for i in a:
            if i in alphanum:
                count+=1
        if count!=b:
            return -1
        else:
            c = lbl_inst[count2]
            if isLineValid(c)!=0 or lineTypesMatch(c)!=0:
                return -2
        count2+=1
    count3 = 0
    b2 = len(lbl_called)
    lbl2 = []
    for i in lbl_declared:
        lbl2.append(i[0])
    for i in lbl_called:
        if i in lbl2:
            count3+=1
    if count3!=b2:
        return -3 
    for i in lbl2:
        if i in inst2:
            return -4
    return 0
def Duplication(lbl_declared,var_declared): #add in main
    count = 0
    count2 = 0
    count3 = 0
    a = len(lbl_declared)
    for i in var_declared:
        if i in lbl_declared:
            count+=1
    for i in range(0,a):
        a2 = lbl_declared[i][0]
        for j in range(i+1,a):
            if a2==lbl_declared[j][0]:
                count2+=1
    if count>0:
        return -1
    if count2>0:
        return -2
    return 0
        
def isLineValid(line_comp):
    """Checks if line is valid that is the instruction is valid and the size corresponds to the instruction"""
    if isInstructionValid(line_comp[0]) == False:
        return -1
    if isSizeRight(line_comp[0], line_comp) == False:
        return -2
    
    return 0


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
        if ls_type_order[i] == 'Memory Address': #start from here
            if line_comp[0]=='ld' or line_comp[0]=='st':
                if line_comp[-1] not in var_declared:
                    if line_comp[-1] in lbl_declared: #illegal use
                        return -5
                    else:
                        return -6
                    
            if line_comp[0]=='jmp' or line_comp[0]=='jlt' or line_comp[0]=='jgt' or line_comp[0]=='je': 
                if line_comp[-1] not in lbl_declared:
                    if line_comp[-1] in var_declared: #illegal use
                        return -7
                    else:
                        return -8
                
                '''else:
                    if isLabelValid(lbl_called,lbl_declared,lbl_inst,inst,alphanum)!=0:
                        return -9'''
            
    return 0
