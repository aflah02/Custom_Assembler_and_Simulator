from OPcode_table import *
from register_and_type_constants import *


def opcode_parser(instruction):
    return OPcode_table[instruction][0]


def immediate_parser(immediate):
    imm = int(immediate[1:])
    return '{0:08b}'.format(imm)

def var_memory_address_parser(location):
    return '{0:08b}'.format(location)

def register_parser(register):
    return register_to_encoding[register]