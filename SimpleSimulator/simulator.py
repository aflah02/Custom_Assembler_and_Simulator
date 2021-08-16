from simulator_parsers import *
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
    
total_lines = 0   
ls_inputs = []
while True:
    try:
        input_line = input()
        ls_inputs.append(input_line)
        total_lines+=1
    except EOFError:
        break

memory_dump_list = ls_inputs.copy()
ls_inputs_length = len(ls_inputs)

for i in range(256 - ls_inputs_length):
    memory_dump_list.append('0'*16)

CYCLE_COUNTER = 0
PROGRAM_COUNTER = 0

PROGRAM_COUNTER_LOCATION = []
CYCLE_COUNTER_VALUES = []

def printOutput(PC, reg_dict, flags_dict):
    PC_val = eight_bit_decimal_to_binary(PC)
    r1_val = sixteen_bit_decimal_to_binary(reg_dict['R1'])
    r2_val = sixteen_bit_decimal_to_binary(reg_dict['R2'])
    r3_val = sixteen_bit_decimal_to_binary(reg_dict['R3'])
    r4_val = sixteen_bit_decimal_to_binary(reg_dict['R4'])
    r5_val = sixteen_bit_decimal_to_binary(reg_dict['R5'])
    r6_val = sixteen_bit_decimal_to_binary(reg_dict['R6'])
    flags_val = '0'*12 + str(flags_dict['V']) + str(flags_dict['L']) + str(flags_dict['G']) + str(flags_dict['E'])
    return_string = f'{PC_val} {r1_val} {r2_val} {r3_val} {r4_val} {r5_val} {r6_val} {flags_val}'
    return return_string

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
        flags['E'] = 0
        flags['V'] = 0
        flags['G'] = 0
        flags['L'] = 0
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
        toPrint = printOutput(PROGRAM_COUNTER, register_tracker, flags)
        print(toPrint)
    elif instruction_type == 'B':
        flags['E'] = 0
        flags['V'] = 0
        flags['G'] = 0
        flags['L'] = 0
        register = encoding_to_register[component_list[1]]
        immediate = immediate_parser(component_list[-1])
        value_to_store = type_b_executor(instruction, register, immediate)
        register_tracker[register] = value_to_store
        toPrint = printOutput(PROGRAM_COUNTER, register_tracker, flags)
        print(toPrint)
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
        toPrint = printOutput(PROGRAM_COUNTER, register_tracker, flags)
        print(toPrint)
    elif instruction_type == 'D':
        flags['E'] = 0
        flags['V'] = 0
        flags['G'] = 0
        flags['L'] = 0
        if instruction == 'ld':
            register_1 = encoding_to_register[component_list[1]]
            mem_add = component_list[2]
            mem_addf = immediate_parser(mem_add)
            value_to_store = ls_inputs[mem_addf]
            value_to_store = value_to_store[8:]
            value_to_storef = immediate_parser(value_to_store)
            register_tracker[register_1] = value_to_store
        if instruction == 'st':
            register_1 = encoding_to_register[component_list[1]]
            mem_add = component_list[2]
            mem_addf = immediate_parser(mem_add)
            value_to_store =  "00000000" + eight_bit_decimal_to_binary(register_tracker[register_1])
            memory_dump_list[total_lines] = value_to_store
            total_lines+=1
        toPrint = printOutput(PROGRAM_COUNTER, register_tracker, flags)
        print(toPrint)
    elif instruction_type == 'E':
        mem_add = binary_instruction[8::]
        mem_addf =  immediate_parser(mem_add)
        if instruction == 'jmp':
            PROGRAM_COUNTER = mem_addf
            flags['E'] = 0
            flags['V'] = 0
            flags['G'] = 0
            flags['L'] = 0
            toPrint = printOutput(PROGRAM_COUNTER, register_tracker, flags)
            print(toPrint)
            continue
        if instruction == 'jlt':
            if flags['L']==1:
                PROGRAM_COUNTER = mem_addf
                flags['E'] = 0
                flags['V'] = 0
                flags['G'] = 0
                flags['L'] = 0
                toPrint = printOutput(PROGRAM_COUNTER, register_tracker, flags)
                print(toPrint)
                continue
        if instruction == 'jgt':
            if flags['G']==1:
                PROGRAM_COUNTER = mem_addf
                flags['E'] = 0
                flags['V'] = 0
                flags['G'] = 0
                flags['L'] = 0
                toPrint = printOutput(PROGRAM_COUNTER, register_tracker, flags)
                print(toPrint)
                continue
        if instruction == 'je':
            if flags['E']==1:
                PROGRAM_COUNTER = mem_addf
                flags['E'] = 0
                flags['V'] = 0
                flags['G'] = 0
                flags['L'] = 0
                toPrint = printOutput(PROGRAM_COUNTER, register_tracker, flags)
                print(toPrint)
                continue
    elif instruction_type == 'F':
        flags['E'] = 0
        flags['V'] = 0
        flags['G'] = 0
        flags['L'] = 0
        if instruction == 'hlt':
            halt_encountered = True
            toPrint = printOutput(PROGRAM_COUNTER, register_tracker, flags)
            print(toPrint)
            continue

    PROGRAM_COUNTER+=1 
    
for i in memory_dump_list:
    print(i)
