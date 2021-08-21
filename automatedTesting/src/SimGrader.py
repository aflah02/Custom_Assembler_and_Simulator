# Simulator Grader class
from utils.colors import bcolors
from Grader import Grader
import os

class SimGrader(Grader):

	SIMPLE_MARKS = 2
	HARD_MARKS = 5

	BIN_HARD_DIR = "hard"
	BIN_SIMPLE_DIR = "simple"

	TRACE_HARD_DIR = "hard"
	TRACE_SIMPLE_DIR = "simple"


	SIM_RUN_DIR = "../SimpleSimulator/"

	def __init__(self, verb, enable):
		super().__init__(verb, enable)
		self.enable = enable

	def handleBin(self, genDir, expDir):
		
		passCount = 0
		totalCount = 0
		
		curDir = os.getcwd()
		tests = self.listFiles("tests/bin/" + genDir)
		tests.sort()
		os.chdir(self.SIM_RUN_DIR)
		
		for test in tests:
			generatedTrace = os.popen("./run < " + "../automatedTesting/tests/bin/" + genDir + "/" + test).readlines()
			expectedTrace = os.popen("cat " + "../automatedTesting/tests/traces/" + expDir + "/" + test).readlines()

			if self.diff(generatedTrace, expectedTrace):
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
			self.printSev(self.HIGH, bcolors.WARNING + bcolors.BOLD + "================ TESTING SIMULATOR ===============" + bcolors.ENDC)
			self.printSev(self.HIGH, bcolors.WARNING + bcolors.BOLD + "==================================================" + bcolors.ENDC)
			self.printSev(self.HIGH, "")
			
			self.printSev(self.HIGH, bcolors.OKBLUE + bcolors.BOLD + "Runing simple tests" + bcolors.ENDC)
			simplePass, simpleTotal = self.handleBin(self.BIN_SIMPLE_DIR, self.TRACE_SIMPLE_DIR)

			self.printSev(self.HIGH, bcolors.OKBLUE + bcolors.BOLD + "\nRunning hard tests" + bcolors.ENDC)
			hardPass, hardTotal = self.handleBin(self.BIN_HARD_DIR, self.TRACE_HARD_DIR)
			
			res = [
					["Simple", simplePass, simpleTotal, self.SIMPLE_MARKS],
					["Hard", hardPass, hardTotal, self.HARD_MARKS],
				]
		
		return res