from datatables import *


def instruction_parser(opcode):
    return opcode_table[opcode][0]


def instruction_type_parser(opcode):
    return opcode_table[opcode][1]


def register_parser(register_code):
    return encoding_to_register[register_code]


def immediate_parser(immediate):
    decimal = 0
    for digit in immediate:
        decimal= decimal*2 + int(digit)
    return decimal

def eight_bit_decimal_to_binary(decimal):
    binary = str(bin(decimal))[2:]
    if len(binary) > 8:
        return binary[-9:-1]
    else:
        return '0'*(8-len(binary)) + binary


def sixteen_bit_decimal_to_binary(decimal):
    binary = str(bin(decimal))[2:]
    if len(binary) > 16:
        return binary[-17:-1]
    else:
        return '0'*(16-len(binary)) + binary