op_code_size = 5
register_size = 3
memory_address_size = 8
immediate_size = 8
ls_instructions = ['add','sub','movi','movr','ld','st','mul','div','rs','ls','xor','or',
'and','not','cmp','jmp','jlt','jgt','je','hlt']
ls_instructions = ['add','sub','mov','ld','st','mul','div','rs','ls','xor','or',
'and','not','cmp','jmp','jlt','jgt','je','hlt']
ls_registers = ['R0','R1','R2','R3','R4','R5','R6','FLAGS']
alphanum = []
for k in range(65,91):
    b = chr(k)
    alphanum.append(b)
for k in range(97,123):
    b = chr(k)
    alphanum.append(b)
for k in range(48,58):
    b = chr(k)
    alphanum.append(b)
alphanum.append(chr(95))
