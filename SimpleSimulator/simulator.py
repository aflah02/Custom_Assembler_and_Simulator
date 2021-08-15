from datatables import *
from helpers import *


register_tracker = {
    'R0': 0,
    'R1': 0,
    'R2': 0,
    'R3': 0,
    'R4': 0,
    'R5': 0,
    'R6': 0,
}

flags = {
    'V':0,
    'L':0,
    'E':0
}

variables = {}

labels = {}

halt_encountered = False

def type_a_executor(instruction, second_register, third_register):
    if instruction == 'add':
        return register_tracker[second_register] + register_tracker[third_register]
    elif instruction == 'sub':
        return register_tracker[second_register] - register_tracker[third_register]
    elif instruction == 'mul':
        return register_tracker[second_register] * register_tracker[third_register]
    elif instruction == 'xor':
        return register_tracker[second_register] ^ register_tracker[third_register]
    elif instruction == 'or':
        return register_tracker[second_register] | register_tracker[third_register]
    elif instruction == 'and':
        return register_tracker[second_register] & register_tracker[third_register]
    elif instruction == 'xor':
        return register_tracker[second_register] ^ register_tracker[third_register]


ls_inputs = []
while True:
    try:
        input_line = input()
        ls_inputs.append(input_line)
    except EOFError:
        break

CYCLE_COUNTER = 0
PROGRAM_COUNTER = 0
PROGRAM_COUNTER_LOCATION = []
CYCLE_COUNTER_VALUE = []

while(halt_encountered == False):
    CYCLE_COUNTER += 1
    binary_instruction = ls_inputs[PROGRAM_COUNTER]
    opcode = binary_instruction[0:4]
    instruction = opcode_table[opcode][0]
    instruction_type = opcode_table[opcode][1]
    component_list = TypeWiseSplitter(binary_instruction, instruction_type)
    if instruction_type == 'A':
        register_1 = encoding_to_register[component_list[1]]
        register_2 = encoding_to_register[component_list[2]]
        register_3 = encoding_to_register[component_list[3]]
        value_to_store = type_a_executor(instruction, register_2, register_3)
        register_tracker[register_1] = value_to_store