import sys
from helper_functions import *

from sys import stdin

ls_inputs = []
for input_line in stdin:
    if input_line == '': # If empty string is read then stop the loop
        break
    ls_inputs.append(input_line)

for line in ls_inputs:
    if not isLineValid(line) or not lineTypeChecks(line):
        print('ERROR')
        break        
    
