'''
type_to_reg_no tells us how many registers are there per type
'''
type_to_reg_no = {
    'A':3,
    'B':1,
    'C':2,
    'D':1,
    'E':0,
    'F':0
}
'''
type_to_input_len tells us how many space separated items will be there per type
'''
type_to_input_len = {
    'A':4,
    'B':3,
    'C':3,
    'D':3,
    'E':2,
    'F':1
}
'''
type_to_imm_no tells us how many immediates are there per type
'''
type_to_imm_no = {
    'A':0,
    'B':1,
    'C':0,
    'D':0,
    'E':0,
    'F':0
}
'''
type_to_unusedbits tells us how many unused bits are there per type
'''
type_to_unusedbits = {
    'A':2,
    'B':0,
    'C':5,
    'D':0,
    'E':3,
    'F':11
}
'''
type_to_memoryaddress tells us how many memory addresses are there per type since at max only 1
can be there this acts as a boolean dict too telling us if the particular instruction type supports memory 
addresses or not
'''
type_to_memoryaddress = {
    'A':0,
    'B':0,
    'C':0,
    'D':1,
    'E':1,
    'F':0
}
'''
register_to_encoding tells us the encoding of a register
'''
register_to_encoding = {
    'R0': '000',
    'R1': '001',
    'R2': '010',
    'R3': '011',
    'R4': '100',
    'R5': '101',
    'R6': '110',
    'FLAGS': '111',
}
'''
type_to_syntaxconstituents tells us about the different type constitutents 
in the syntax and their order like registers, immediates, etc.
'''
type_to_syntaxconstituents = {
    'A':['Instruction','Register','Register','Register'],
    'B':['Instruction','Register','Immediate'],
    'C':['Instruction','Register','Register'],
    'D':['Instruction','Register','Memory Address'],
    'E':['Instruction','Memory Address'],
    'F':['Instruction']
}