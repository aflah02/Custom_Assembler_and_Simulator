from simulator_parsers import *
from datatables import *
from helpers import *
import datetime
import plotly.graph_objects as go

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
        right_shifted_value = register_tracker[first_register] >> immediate
        sixteen_bits_last = sixteen_bit_decimal_to_binary(right_shifted_value)
        right_shifted_value_to_be_returned = binary_to_decimal_parser(sixteen_bits_last)
        return right_shifted_value_to_be_returned
    elif instruction == 'ls':
        left_shifted_value = register_tracker[first_register] >> immediate
        sixteen_bits_last = sixteen_bit_decimal_to_binary(left_shifted_value)
        left_shifted_value_to_be_returned = binary_to_decimal_parser(sixteen_bits_last)
        return left_shifted_value_to_be_returned

def type_c_executor(instruction, first_register, second_register, flags_dict):
    if instruction == 'movr':
        if second_register == 'FLAGS':
            return binary_to_decimal_parser('0'*12 + str(flags_dict['V']) + str(flags_dict['L']) + str(flags_dict['G']) + str(flags_dict['E']))
        else:
            return register_tracker[second_register]
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
    r0_val = sixteen_bit_decimal_to_binary(reg_dict['R0'])
    r1_val = sixteen_bit_decimal_to_binary(reg_dict['R1'])
    r2_val = sixteen_bit_decimal_to_binary(reg_dict['R2'])
    r3_val = sixteen_bit_decimal_to_binary(reg_dict['R3'])
    r4_val = sixteen_bit_decimal_to_binary(reg_dict['R4'])
    r5_val = sixteen_bit_decimal_to_binary(reg_dict['R5'])
    r6_val = sixteen_bit_decimal_to_binary(reg_dict['R6'])
    flags_val = '0'*12 + str(flags_dict['V']) + str(flags_dict['L']) + str(flags_dict['G']) + str(flags_dict['E'])
    return_string = f'{PC_val} {r0_val} {r1_val} {r2_val} {r3_val} {r4_val} {r5_val} {r6_val} {flags_val}'
    return return_string

while(halt_encountered == False):
    CYCLE_COUNTER_VALUES.append(CYCLE_COUNTER)
    PROGRAM_COUNTER_LOCATION.append(PROGRAM_COUNTER)
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
            if value_to_store > pow(2,16)-1 or value_to_store < 0:
                flags['V'] = 1
                binary_overflowed_last_sixteen_bits = sixteen_bit_decimal_to_binary(value_to_store)
                register_tracker[register_1] = binary_to_decimal_parser(binary_overflowed_last_sixteen_bits)
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
        immediate = binary_to_decimal_parser(component_list[-1])
        value_to_store = type_b_executor(instruction, register, immediate)
        register_tracker[register] = value_to_store
        toPrint = printOutput(PROGRAM_COUNTER, register_tracker, flags)
        print(toPrint)
    elif instruction_type == 'C':
        first_register = encoding_to_register[component_list[1]]
        second_register = encoding_to_register[component_list[-1]]
        value_to_store = type_c_executor(instruction, first_register, second_register, flags)
        if instruction == 'movr':
            register_tracker[first_register] = value_to_store
            flags['E'] = 0
            flags['V'] = 0
            flags['G'] = 0
            flags['L'] = 0
        elif instruction == 'not':
            flags['E'] = 0
            flags['V'] = 0
            flags['G'] = 0
            flags['L'] = 0
            register_tracker[first_register] = value_to_store
        elif instruction == 'div':
            flags['E'] = 0
            flags['V'] = 0
            flags['G'] = 0
            flags['L'] = 0
            register_tracker['R0'], register_tracker['R1'] = value_to_store
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
            mem_addf = binary_to_decimal_parser(mem_add)
            value_to_store = memory_dump_list[mem_addf]
            value_to_store = value_to_store[8:]
            value_to_storef = binary_to_decimal_parser(value_to_store)
            register_tracker[register_1] = value_to_storef
            PROGRAM_COUNTER_LOCATION.append(mem_addf)
            CYCLE_COUNTER_VALUES.append(CYCLE_COUNTER)
        if instruction == 'st':
            register_1 = encoding_to_register[component_list[1]]
            mem_add = component_list[2]
            mem_addf = binary_to_decimal_parser(mem_add)
            value_to_store =  "00000000" + eight_bit_decimal_to_binary(register_tracker[register_1])
            memory_dump_list[mem_addf] = value_to_store
            PROGRAM_COUNTER_LOCATION.append(mem_addf)
            CYCLE_COUNTER_VALUES.append(CYCLE_COUNTER)
        toPrint = printOutput(PROGRAM_COUNTER, register_tracker, flags)
        print(toPrint)
    elif instruction_type == 'E':
        mem_add = binary_instruction[8::]
        mem_addf =  binary_to_decimal_parser(mem_add)
        if instruction == 'jmp':
            PROGRAM_COUNTER = mem_addf
            flags['E'] = 0
            flags['V'] = 0
            flags['G'] = 0
            flags['L'] = 0
            toPrint = printOutput(PROGRAM_COUNTER, register_tracker, flags)
            print(toPrint)
            CYCLE_COUNTER+=1
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
                CYCLE_COUNTER+=1
                continue
            else:
                flags['E'] = 0
                flags['V'] = 0
                flags['G'] = 0
                flags['L'] = 0
                toPrint = printOutput(PROGRAM_COUNTER, register_tracker, flags)
                print(toPrint)
        if instruction == 'jgt':
            if flags['G']==1:
                PROGRAM_COUNTER = mem_addf
                flags['E'] = 0
                flags['V'] = 0
                flags['G'] = 0
                flags['L'] = 0
                toPrint = printOutput(PROGRAM_COUNTER, register_tracker, flags)
                print(toPrint)
                CYCLE_COUNTER+=1
                continue
            else:
                flags['E'] = 0
                flags['V'] = 0
                flags['G'] = 0
                flags['L'] = 0
                toPrint = printOutput(PROGRAM_COUNTER, register_tracker, flags)
                print(toPrint)
        if instruction == 'je':
            if flags['E']==1:
                PROGRAM_COUNTER = mem_addf
                flags['E'] = 0
                flags['V'] = 0
                flags['G'] = 0
                flags['L'] = 0
                toPrint = printOutput(PROGRAM_COUNTER, register_tracker, flags)
                print(toPrint)
                CYCLE_COUNTER+=1
                continue
            else:
                flags['E'] = 0
                flags['V'] = 0
                flags['G'] = 0
                flags['L'] = 0
                toPrint = printOutput(PROGRAM_COUNTER, register_tracker, flags)
                print(toPrint) 
    elif instruction_type == 'F':
        flags['E'] = 0
        flags['V'] = 0
        flags['G'] = 0
        flags['L'] = 0
        if instruction == 'hlt':
            halt_encountered = True
            toPrint = printOutput(PROGRAM_COUNTER, register_tracker, flags)
            print(toPrint)
            CYCLE_COUNTER+=1
            continue

    PROGRAM_COUNTER+=1 
    CYCLE_COUNTER+=1
    
for i in range(len(memory_dump_list)):
    print(memory_dump_list[i])

for i in range(len(CYCLE_COUNTER_VALUES)):
    CYCLE_COUNTER_VALUES[i] += 1

time = datetime.datetime.now()
file_name = str(time)
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=CYCLE_COUNTER_VALUES,
    y=PROGRAM_COUNTER_LOCATION,
    mode="markers",
    marker=dict(
        color='steelblue',
        size=5,
        line=dict(
            color='steelblue',
            width=2
        )
    )
))
fig.update_layout(
    title = {
        'text' : 'Memory Address v/s Cycle Number',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    width=1000,
    height=1000,
    font_family="Times New Roman",
    font_color="red",
    title_font_family="Times New Roman",
    title_font_color="black",
    xaxis_title="Cycle Number",
    yaxis_title="Program Counter",
)
fig.write_image(f"images/{file_name}.png")