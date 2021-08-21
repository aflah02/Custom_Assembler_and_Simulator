# Result generator class

from utils.colors import bcolors

class Results:

	VERBOSE = False
	asmRes = None
	simRes = None


	def declareARes(self, res):
		print(bcolors.HEADER, end="")
		
		totalMarksGained = 0
		totalMarks = 0
		for suite in res:
			print(suite[0], end=": ")
			print("Marks =", suite[1] * suite[-1], "out of", suite[2] * suite[-1])
			if(self.VERBOSE):
				print("Passed", suite[1], "out of", suite[2], "tests")

			totalMarksGained += suite[1] * suite[-1]
			totalMarks += suite[2] * suite[-1]

		print(bcolors.BOLD + bcolors.OKGREEN + "Total: " + str(totalMarksGained) + " out of " + str(totalMarks))
		print(bcolors.ENDC, end="")

	def declare(self):
		print("\n============== RESULTS =================\n")
		if(self.asmRes):
			print("Assembler ===>")
			self.declareARes(self.asmRes)
		if(self.simRes):
			print("Simulator ===>")
			self.declareARes(self.simRes)

	def __init__(self, verb, asmRes, simRes):
		self.VERBOSE = verb
		self.asmRes = asmRes
		self.simRes = simRes