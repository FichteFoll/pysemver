# import re


class SemVer(object):
	disallowed_chars = "-_ v="

	def parse(self, term):
		data = []
		for piece in term.split("."):
			if piece.isdigit():
				piece = int(piece)
				data.append(piece)
			else:
				for each in piece.split("-"):
					piece.strip(self.disallowed_chars)
					if piece.isdigit():
						piece = int(piece)
					data.append(each)
		return data

	def gt(self, v1, v2):
		v1 = self.parse(v1)
		v2 = self.parse(v2)
		for x in range(1, max(len(v1), len(v2))):
			if v1[x] > v2[x]:
				return True
			elif v1[x] == v2[x]:
				pass
			else:
				return False

	# function stringify (version)
	# function clean (version)
	# function valid (version)
	# function validPackage (version)
	# function toComparators (range)
	# function replaceStars (stars)
	# function replaceXRanges (ranges)
	# function replaceXRange (version)
	# function replaceSpermies (version)
	# function validRange (range)
	# function maxSatisfying (versions, range)
	# function satisfies (version, range)
	# function compare (v1, v2)
	# function rcompare (v1, v2)
	# function lt (v1, v2) { return gt(v2, v1); }
	# function gte (v1, v2) { return !lt(v1, v2); }
	# function lte (v1, v2) { return !gt(v1, v2); }
	# function eq (v1, v2) { return gt(v1, v2); }
	# function neq (v1, v2) { return gt(v1, v2); }
	# function cmp (v1, c, v2)
	# function num (v)
	# function gt (v1, v2)
	# function inc (version, release)

	# sv_major = r"\s*[v=]*\s*([0-9]+)"
	# sv_minor = r"\.([0-9]+)"
	# sv_patch = r"\.([0-9]+)"
	# sv_build = r"(-[0-9]+-?)?"
	# sv_tag = r"([a-zA-Z-+][a-zA-Z0-9-\.:]*)?"
	# semver = sv_major + sv_minor + sv_patch + sv_build + sv_tag
	# exprComparator = r"^((<|>)?=?)\s*(" + semver + r")$|^$"
	# xRangePlain = r"[v=]*([0-9]+|x|X|\*)" + r"(?:\.([0-9]+|x|X|\*)" + r"(?:\.([0-9]+|x|X|\*)" + r"([a-zA-Z-][a-zA-Z0-9-\.:]*)?)?)?"
	# xRange = r"((?:<|>)=?)?\s*" + xRangePlain
	# exprSpermy = r"(?:~>?)" + xRange
	# parse = re.compile(r"^\s*" + semver + r"\s*$")
	# parsePackage = re.compile(r"^\s*([^\/]+)[-@](" + semver + r")\s*$")
	# parseRange = re.compile(r"^\s*(" + semver + r")\s+-\s+(" + semver + r")\s*$")
	# validComparator = re.compile(r"^" + exprComparator + r"$")
	# parseXRange = re.compile(r"^" + xRange + r"$")
	# parseSpermy = re.compile(r"^" + exprSpermy + r"$")
	# parseInts = re.compile(r"\d*")

	# def gt(self, v1, v2):
	# 	v1 = self.parse.match(v1)
	# 	v2 = self.parse.match(v2)

	# 	if not v1 or not v2:
	# 		return False
	# 	for x in range(1, 5):
	# 		one = v1.group(x)
	# 		two = v2.group(x)
	# 		if one == None and two != None:
	# 			return True
	# 		elif one != None and two == None:
	# 			return False
	# 		elif one == None and two == None:
	# 			return False
	# 		if self.parseInts.match(one):
	# 			one = int(one)
	# 		if self.parseInts.match(two):
	# 			two = int(two)
	# 		if one > two:
	# 			return True
	# 		elif one != two:
	# 			return False

	# def lt(self, v1, v2):
	# 	return not self.gt(v1, v2)
