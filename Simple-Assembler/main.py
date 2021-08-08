import sys
from helper_functions import *
from OPcode_table import *
from register_and_type_constants import *
from sys import stdin

ls_inputs = []
for input_line in stdin:
    if input_line == '': # If empty string is read then stop the loop
        break
    ls_inputs.append(input_line)

VALID = True
error_tracker = []

for line in ls_inputs:
    line_comps = list(map(str, line.split()))
    if isLineValid(line) == -1:
        error_tracker.append(f'ERROR: No Such Instruction Found as {line_comps[0]}')
        VALID = False
        break
    if isLineValid(line) == -2:
        error_tracker.append(f'ERROR: Wrong Syntax used for Instruction {line_comps[0]}, please note it is a Type {OPcode_table[line_comps[0]]} which requires {type_to_input_len[line_comps[0]]} arguments including the instruction')
        VALID = False
        break
    if lineTypesMatch(line) ==  -1:
        error_tracker.append(f'ERROR (Invalid Register): Wrong Syntax used for Instruction {line_comps[0]}, kindly use acceptable argument(s) only which in case of {line_comps[0]} is/are {type_to_syntaxconstituents[OPcode_table[line_comps[0]]]}')
        VALID = False
        break
    if lineTypesMatch(line) ==  -2:
        error_tracker.append(f'ERROR (Invalid Immediate): Wrong Syntax used for Instruction {line_comps[0]}, kindly use acceptable argument(s) only which in case of {line_comps[0]} is/are {type_to_syntaxconstituents[OPcode_table[line_comps[0]]]}')
        VALID = False
        break
    