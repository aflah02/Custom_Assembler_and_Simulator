# Parent class for all graders
from os import listdir
from os.path import isfile, join
from utils.colors import bcolors

class Grader:

	verbose = False
	enable = False
	
	# Printing severity
	HIGH = 1 	# Printed even if not verbose
	LOW = 0

	def printSev(self, sev, string, end = "\n"):
		if sev == self.HIGH or self.verbose:
			print(string, end=end)

	def listFiles(self, dirPath):
		return [f for f in listdir(dirPath) if isfile(join(dirPath, f))]


	def diff(self, lines1, lines2):
		lines1Clean = []
		lines2Clean = []

		for l in lines1:
			if l.strip() != "":
				lines1Clean.append(l.strip())

		for l in lines2:
			if l.strip() != "":
				lines2Clean.append(l.strip())

		match = True

		# Match Size
		if(len(lines1Clean) > len(lines2Clean)):
			lines2Clean += [""] * (len(lines1Clean) - len(lines2Clean))
		elif(len(lines2Clean) > len(lines1Clean)):
			lines1Clean += [""] * (len(lines2Clean) - len(lines1Clean))

		for lineNum, lines in enumerate(zip(lines1Clean, lines2Clean), 1):
			if(lines[0] != lines[1]):
				self.printSev(self.LOW, bcolors.FAIL + "Mismatch at line " + str(lineNum) +  "." + bcolors.ENDC)
				match &= False

		return match

	def __init__(self, verb, enable):
		self.verbose = verb
		self.enable = enable
	
	def grade(self):
		raise NotImplementedError("Please Implement this method")