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
    if (instruction == 'add'):
        return register_tracker[second_register] + register_tracker[third_register]
    elif (instruction == 'sub'):
        return register_tracker[second_register] - register_tracker[third_register]
    pass

ls_inputs = []
while True:
    try:
        input_line = input()
        ls_inputs.append(input_line)
    except EOFError:
        break

while(halt_encountered == False):
    pass