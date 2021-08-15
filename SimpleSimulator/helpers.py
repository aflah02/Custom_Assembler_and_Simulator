from datatables import *
from simulator import *

def TypeWiseSplitter(instruction, instruction_type):
    syntax_constituents = type_to_syntaxconstituents[instruction_type]
    unused_bits = type_to_unusedbits[instruction_type]
    component_list = []
    component_list.append(instruction[0:5])
    if instruction_type == 'A':
        component_list.append(instruction[7:10])
        component_list.append(instruction[10:13])
        component_list.append(instruction[13:16])
    elif instruction_type == 'B':
        component_list.append(instruction[7:10])
        component_list.append(instruction[10:])
    elif instruction_type == 'C':
        component_list.append(instruction[10:13])
        component_list.append(instruction[13:16])
    elif instruction_type == 'D':
        component_list.append(instruction[5:8])
        component_list.append(instruction[8:16])
    elif instruction_type == 'E':
        component_list.append(instruction[8:16])
    elif instruction_type == 'F':
        pass
    return component_list