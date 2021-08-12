from OPcode_table import *
from register_and_type_constants import *


def opcode_parser(instruction):
    """Parses OPCODE for Given Instruction"""
    return OPcode_table[instruction][0]


def immediate_parser(immediate):
    """Parses Binary Value for Given Immediate"""
    imm = int(immediate[1:])
    return '{0:08b}'.format(imm)

def memory_address_parser(location):
    """Parses Binary Value for Given Memory Address"""
    return '{0:08b}'.format(location)

def register_parser(register):
    """Parses Register Encoding for Given Register Name"""
    return register_to_encoding[register]