# Runs automated tests for assembler and simulator

import sys
from utils.colors import bcolors
from AsmGrader import AsmGrader
from SimGrader import SimGrader
from Results import Results


VERBOSE = False
GRADE_ASSEMBLER = True
GRADE_SIMULATOR = True

def printHelp():
	print("--verbose for verbose output")
	print("--no-asm to not grade assembler")
	print("--no-sim to not grade simulator")

def setupArgs():
	global VERBOSE
	global GRADE_ASSEMBLER
	global GRADE_SIMULATOR

	for arg in sys.argv[1:]:
		if arg == "--verbose":
			VERBOSE = True
		elif arg == "--no-asm":
			GRADE_ASSEMBLER = False
		elif arg == "--no-sim":
			GRADE_SIMULATOR = False
		else:
			printHelp()
			break

def main():
	setupArgs()

	asmGrader = AsmGrader(VERBOSE, GRADE_ASSEMBLER)
	simGrader = SimGrader(VERBOSE, GRADE_SIMULATOR)

	asmRes = asmGrader.grade()
	simRes = simGrader.grade()	

	res = Results(VERBOSE, asmRes, simRes)
	res.declare()

if __name__ == '__main__':
	main()