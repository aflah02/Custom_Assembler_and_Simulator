import sys
from helper_functions import *

from sys import stdin

ls_inputs = []
for input_line in stdin:
    if input_line == '': # If empty string is read then stop the loop
        break
    ls_inputs.append(input_line)

# for input in ls_inputs:
