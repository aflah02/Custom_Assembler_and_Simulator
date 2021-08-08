# Assembler Grader class
from utils.colors import bcolors
from Grader import Grader
import os

class AsmGrader(Grader):

	SIMPLE_MARKS = 2
	HARD_MARKS = 5

	ASM_ERROR_DIR = "errorGen"
	ASM_HARD_DIR = "hardBin"
	ASM_SIMPLE_DIR = "simpleBin"

	BIN_HARD_DIR = "hard"
	BIN_SIMPLE_DIR = "simple"

	ASM_RUN_DIR = "../Simple-Assembler/"

	def __init__(self, verb, enable):
		super().__init__(verb, enable)
		self.enable = enable

	def handleErrorGen(self):
	
		curDir = os.getcwd()
		tests = self.listFiles("tests/assembly/" + self.ASM_ERROR_DIR)
		tests.sort()
		os.chdir(self.ASM_RUN_DIR)
		
		for test in tests:
			self.printSev(self.HIGH, bcolors.OKCYAN + "Running " + test + bcolors.ENDC)
			errors = os.popen("./run < " + "../automatedTesting/tests/assembly/" + self.ASM_ERROR_DIR + "/" + test).read()
			self.printSev(self.HIGH, errors, end="")
			self.printSev(self.HIGH, "============================================\n")

		os.chdir(curDir)

	def handleBin(self, genDir, expDir):
		
		passCount = 0
		totalCount = 0
		
		curDir = os.getcwd()
		tests = self.listFiles("tests/assembly/" + genDir)
		tests.sort()
		os.chdir(self.ASM_RUN_DIR)
		
		for test in tests:
			generatedBin = os.popen("./run < " + "../automatedTesting/tests/assembly/" + genDir + "/" + test).readlines()
			expectedBin = os.popen("cat " + "../automatedTesting/tests/bin/" + expDir + "/" + test).readlines()

			if self.diff(generatedBin, expectedBin):
				self.printSev(self.HIGH, bcolors.OKGREEN + "[PASSED]" + bcolors.ENDC + " " + test)
				passCount += 1
			else:
				self.printSev(self.HIGH, bcolors.FAIL + "[FAILED]" + bcolors.ENDC + " " + test)
			totalCount += 1

		os.chdir(curDir)
		return passCount, totalCount
	
	def grade(self):
		res = None
		if(self.enable):
			self.printSev(self.HIGH, bcolors.WARNING + bcolors.BOLD + "==================================================" + bcolors.ENDC)
			self.printSev(self.HIGH, bcolors.WARNING + bcolors.BOLD + "================ TESTING ASSEMBLER ===============" + bcolors.ENDC)
			self.printSev(self.HIGH, bcolors.WARNING + bcolors.BOLD + "==================================================" + bcolors.ENDC)
			self.printSev(self.HIGH, "")
			
			self.printSev(self.HIGH, bcolors.OKBLUE + bcolors.BOLD + "Runing simple tests" + bcolors.ENDC)
			simplePass, simpleTotal = self.handleBin(self.ASM_SIMPLE_DIR, self.BIN_SIMPLE_DIR)

			self.printSev(self.HIGH, bcolors.OKBLUE + bcolors.BOLD + "\nRunning hard tests" + bcolors.ENDC)
			hardPass, hardTotal = self.handleBin(self.ASM_HARD_DIR, self.BIN_HARD_DIR)
			
			self.printSev(self.HIGH, bcolors.OKBLUE + bcolors.BOLD + "Running error tests" + bcolors.ENDC)
			self.handleErrorGen()
			res = [
					["Simple", simplePass, simpleTotal, self.SIMPLE_MARKS],
					["Hard", hardPass, hardTotal, self.HARD_MARKS],
				]
		
		return res