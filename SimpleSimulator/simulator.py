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

ls_inputs = []
while True:
    try:
        input_line = input()
        ls_inputs.append(input_line)
    except EOFError:
        break

while(halt_encountered == False):
    pass