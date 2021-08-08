from general_consts import *
from register_and_type_constants import *


def getRegisterEncoding(register):
    """Returns Register Encoding"""
    return register_to_encoding[register]


def getRegisterCount(type):
    """Returns Register Count"""
    return type_to_reg_no[type]