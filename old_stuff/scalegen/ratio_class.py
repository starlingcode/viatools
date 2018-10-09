#!/usr/bin/python


class ratio:
	def __init__(self, ratioString):
		self.num = int(ratioString[0:ratioString.index("/")])
		if "-" in ratioString:
			self.den = int(ratioString[ratioString.index("/") + 1 : ratioString.index("-")])
			self.divisor = int(ratioString[ratioString.index("-") + 1 :])
			self.gcd = int(math.gcd(self.num, self.den))
		else:
			self.den = int(ratioString[ratioString.index("/") + 1:])
			self.gcd = int(math.gcd(self.num, self.den))
			self.divisor = int(self.den / self.gcd)
		self.num = int(self.num / self.gcd)
		self.den = int(self.den / self.gcd)
		self.integer = int(self.num * 2 ** 48 / self.den) >> 32
		self.frac = int(self.num * 2 ** 48) - (self.integer << 32)
		self.tag = "ratio" + str(self.num) + "_" + str(self.den) + "-" + str(self.divisor)
		self.log = math.log(self.num / self.den)
	def __str__(self):
		return self.tag
	def val(self):
		return float(self.num / self.den)
	def octave(self, shiftSize):
		if shiftSize < 0:
			return self.__class__(str(self.num * 2 * shiftSize) + "/" + str(self.den))
		else:
			return self.__class__(str(self.num) + "/" + str(self.den * 2 * shiftSize))
	def tritave(self, shiftSize):
		if shifSize < 0:
			return self.__class__(str(self.num * 3 * shiftSize) + "/" + str(self.den))
		else:
			return self.__class__(str(self.num) + "/" + str(self.den * 3 * shiftSize))

class scaleRow(ratio):
	def __init__(self, rowString):
		self.elements = csv.reader(self.rowString, delimiter = ',' quotechar = '|')
		self.name = self.elements[0]
		for element in self.elements[1:]:
			self.ratios[].append(ratio(element))
	def __str__(self):
		return self.name
	def len(self):
		return len(self.ratios)
	def upperOctBound(self):
		return ceiling(max(self.ratios.log))
	def lowerOctBound(self:
		return floor(min(self.ratios.log))

		
class scaleFamily(scaleRow):
	def __init__(self, scaleName)
		with open(scaleName + ".csv", newline="\n") as csvfile:
			for line in csvfile
				self.scaleRows.append(self.scaleRow(line)
	def __str__(self):
		return self.scaleName
	def len(self):
		return len(csvfile)

