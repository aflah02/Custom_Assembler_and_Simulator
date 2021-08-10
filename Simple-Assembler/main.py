import sys
from helper_functions import *
from OPcode_table import *
from register_and_type_constants import *
from sys import stdin

ls_inputs = []
for input_line in stdin:
    if input_line == '\n':
        break
    ls_inputs.append(input_line[:-1])

VALID = True
HLT_COUNT = 0
error_tracker = []
LINE_COUNT = 1
LINE_COUNT2 = 1
LINE_COUNT3 = 1
var_declared = []
var_called = []
lbl_declared = []
lbl_called = []
lbl_instf = []
for line in ls_inputs:
    line = line.strip()
    line_comp = list(map(str, line.split()))
    a = line_comp[0]
    b = len(line_comp)
    lbl_inst = []
    for i in range(1,b):
        lbl_inst.append(i)
    lbl_instf.append(lbl_inst)
    if a[-1::] == ":":
        b = a[:-1:]
        c = LINE_COUNT2
        d = (b,c)
        lbl_declared.append(d)
        
for line in ls_inputs:
    line = line.strip()
    line_comp = list(map(str, line.split()))
    a = line_comp[0]
    if a[-1::] == ":":
        if line_comp[1]=='ld' or line_comp[1]=='st':
            b = line_comp[-1]
            var_called.append(b)
        if line_comp[1]=='jmp' or line_comp[1]=='jlt' or line_comp[1]=='jgt' or line_comp[1]=='je':
            b = line_comp[-1]
            lbl_called.append(b)
    if line_comp[0]=='ld' or line_comp[0]=='st':
        b = line_comp[-1]
        var_called.append(b)
    if line_comp[0]=='jmp' or line_comp[0]=='jlt' or line_comp[0]=='jgt' or line_comp[0]=='je': 
        b = line_comp[-1]
        lbl_called.append(b)

for line in ls_inputs:
    line = line.strip()
    line_comp = list(map(str, line.split()))
    if len(line_comp)==2:
        if line_comp[0] == "var":
            b = line_comp[-1]
            c = (b,LINE_COUNT3)
            var_declared.append(c)
    LINE_COUNT3+=1
if isVarValid(var_declared,var_called,alphanum,ls_instructions) == -1:
    error_tracker.append(f'ERROR (Variable): Illegal declaration of variables')
    VALID = False 
if isVarValid(var_declared,var_called,alphanum,ls_instructions) == -2:
    error_tracker.append(f'ERROR (Variable): Variable name incorrect')
    VALID = False   
if isVarValid(var_declared,var_called,alphanum,ls_instructions) == -3:
    error_tracker.append(f'ERROR (Variable): Variable called was never declared')
    VALID = False 
if isVarValid(var_declared,var_called,alphanum,ls_instructions) == -4:
    error_tracker.append(f'ERROR (Variable): Variable has the same name as an ISA instruction')
    VALID = False
    
if isLabelValid(lbl_called,lbl_declared,lbl_inst,ls_instructions,alphanum) == -1:
    error_tracker.append(f'ERROR (Label): Invalid label name')
    VALID = False
if isLabelValid(lbl_called,lbl_declared,lbl_inst,ls_instructions,alphanum) == -2:
    error_tracker.append(f'ERROR (Label): Invalid label instruction')
    VALID = False
if isLabelValid(lbl_called,lbl_declared,lbl_inst,ls_instructions,alphanum) == -3:
    error_tracker.append(f'ERROR (Label): Invalid label called')
    VALID = False
if isLabelValid(lbl_called,lbl_declared,lbl_inst,ls_instructions,alphanum) == -4:
    error_tracker.append(f'ERROR (Label): Label name is the same as an instruction')
    VALID = False

if Duplication(lbl_declared,var_declared)==-1:
    error_tracker.append(f'ERROR (Label/Var): Label name is the same as a variable')
    VALID = False
if Duplication(lbl_declared,var_declared)==-2:
    error_tracker.append(f'ERROR (Label): A label was declared more than once')
    VALID = False
if Duplication(lbl_declared,var_declared)==-3:
    error_tracker.append(f'ERROR (Var): A variable was declared more than once')
    VALID = False
    
for line in ls_inputs:
    line = line.strip()
    line_comp = list(map(str, line.split()))
    a = line_comp[0]
    if a[-1::]==':':
        continue
    if line_comp[0]=="var":
        LINE_COUNT-=1
        continue
    if isLineValid(line_comp) == -1:
        error_tracker.append(f'ERROR: No Such Instruction Found as {line_comp[0]}')
        VALID = False
        break
    if isLineValid(line_comp) == -2:
        error_tracker.append(f'ERROR: Wrong Syntax used for Instruction {line_comp[0]}, please note it is a Type {OPcode_table[line_comp[0]]} which requires {type_to_input_len[line_comp[0]]} arguments including the instruction')
        VALID = False
        break
    if lineTypesMatch(line_comp,lbl_declared,var_declared) == -1:
        error_tracker.append(f'ERROR (Invalid Register (No such Register Found)): Wrong Syntax used for Instruction {line_comp[0]}, kindly use acceptable argument(s) only which in case of {line_comp[0]} is/are {type_to_syntaxconstituents[OPcode_table[line_comp[0]]]}')
        VALID = False
        break
    if lineTypesMatch(line_comp,lbl_declared,var_declared) == -2:
        error_tracker.append(f'ERROR (Invalid Immediate (Not Starting with $)): Wrong Syntax used for Instruction {line_comp[0]}, kindly use acceptable argument(s) only which in case of {line_comp[0]} is/are {type_to_syntaxconstituents[OPcode_table[line_comp[0]]]}')
        VALID = False
        break
    if lineTypesMatch(line_comp,lbl_declared,var_declared) == -3:
        error_tracker.append(f'ERROR (Invalid Immediate (Out of Range)): Kindly use Immediates between 0 and 255 (Inclusive of both Limits)')
        VALID = False
        break
    if lineTypesMatch(line_comp,lbl_declared,var_declared) == -4:
        error_tracker.append(f'ERROR Invalid use of FLAGS register')
        VALID = False
        break
    if lineTypesMatch(line_comp,lbl_declared,var_declared) == -5 or lineTypesMatch(line_comp,lbl_declared,var_declared) == -8:
        error_tracker.append(f'ERROR Invalid use of label')
        VALID = False
        break
    if lineTypesMatch(line_comp,lbl_declared,var_declared) == -6 or lineTypesMatch(line_comp,lbl_declared,var_declared) == -7:
        error_tracker.append(f'ERROR Invalid use of variable')
        VALID = False
        break
    if 'hlt' in line_comp:
        HLT_COUNT += 1
    
    LINE_COUNT+=1

if HLT_COUNT == 0:
    error_tracker.append(f'ERROR (hlt): No hlt instruction present')
    VALID = False

if HLT_COUNT > 1:
    error_tracker.append(f'ERROR (hlt): Multiple hlt instruction present')
    VALID = False

if HLT_COUNT == 1 and ls_inputs[-1] != 'hlt':
    error_tracker.append(f'ERROR (hlt): hlt not present as last instruction')
    VALID = False