from SimpleSimulator.simulator_parsers import decimal_to_binary, immediate_parser
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
    'G':0,
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

def type_b_executor(instruction, first_register, immediate):
    if instruction == 'movi':
        return immediate
    elif instruction == 'rs':
        return register_tracker[first_register] >> immediate
    elif instruction == 'ls':
        return register_tracker[first_register] << immediate

def type_c_executor(instruction, first_register, second_register):
    if instruction == 'movr':
        return second_register
    elif instruction == 'div':
        a, b = register_tracker[first_register], register_tracker[second_register]
        return (a//b, a%b)
    elif instruction == 'not':
        return ~(register_tracker[second_register])
    elif instruction == 'cmp':
        a, b = register_tracker[first_register], register_tracker[second_register]
        if a==b:
            return "E"
        elif a<b:
            return "L"
        else:
            return "G"

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
CYCLE_COUNTER_VALUES = []

while(halt_encountered == False):
    CYCLE_COUNTER_VALUES.append(CYCLE_COUNTER)
    PROGRAM_COUNTER_LOCATION.append(PROGRAM_COUNTER)
    CYCLE_COUNTER += 1
    binary_instruction = ls_inputs[PROGRAM_COUNTER]
    opcode = binary_instruction[0:5]
    instruction = opcode_table[opcode][0]
    instruction_type = opcode_table[opcode][1]
    component_list = TypeWiseSplitter(binary_instruction, instruction_type)
    if instruction_type == 'A':
        register_1 = encoding_to_register[component_list[1]]
        register_2 = encoding_to_register[component_list[2]]
        register_3 = encoding_to_register[component_list[3]]
        value_to_store = type_a_executor(instruction, register_2, register_3)
        if instruction == 'add' or instruction == 'sub' or instruction == 'mul':
            if value_to_store > 255 or value_to_store < 0:
                flags['V'] = 1
            else:
                register_tracker[register_1] = value_to_store
        else:
            register_tracker[register_1] = value_to_store
    elif instruction_type == 'B':
        register = encoding_to_register[component_list[1]]
        immediate = immediate_parser(component_list[-1])
        value_to_store = type_b_executor(instruction, register, immediate)
        register_tracker[register] = value_to_store
    elif instruction_type == 'C':
        first_register = encoding_to_register[component_list[1]]
        second_register = encoding_to_register[component_list[-1]]
        value_to_store = type_c_executor(instruction, first_register, second_register)
        if instruction == 'movr' or instruction == 'not':
            register_tracker[first_register] = value_to_store
        elif instruction == 'div':
            register_tracker[first_register], register_tracker[second_register] = value_to_store
        elif instruction == 'cmp':
            flags[value_to_store] = 1