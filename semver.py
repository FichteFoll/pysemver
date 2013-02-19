import re


class SemVer(object):
	"""docstring for SemVer"""

	sv_major = r"\s*[v=]*\s*([0-9]+)"
	sv_minor = r"\.([0-9]+)"
	sv_patch = r"\.([0-9]+)"
	sv_build = r"(-[0-9]+-?)?"
	sv_tag = r"([a-zA-Z-+][a-zA-Z0-9-\.:]*)?"
	semver = sv_major + sv_minor + sv_patch + sv_build + sv_tag
	exprComparator = r"^((<|>)?=?)\s*(" + semver + r")$|^$"
	xRangePlain = r"[v=]*([0-9]+|x|X|\*)" + r"(?:\.([0-9]+|x|X|\*)" + r"(?:\.([0-9]+|x|X|\*)" + r"([a-zA-Z-][a-zA-Z0-9-\.:]*)?)?)?"
	xRange = r"((?:<|>)=?)?\s*" + xRangePlain
	exprSpermy = r"(?:~>?)" + xRange
	parse = re.compile(r"^\s*" + semver + r"\s*$")
	parsePackage = re.compile(r"^\s*([^\/]+)[-@](" + semver + r")\s*$")
	parseRange = re.compile(r"^\s*(" + semver + r")\s+-\s+(" + semver + r")\s*$")
	validComparator = re.compile(r"^" + exprComparator + r"$")
	parseXRange = re.compile(r"^" + xRange + r"$")
	parseSpermy = re.compile(r"^" + exprSpermy + r"$")

	def __init__(self):
		super(SemVer, self).__init__()

	def gt(self, v1, v2):
		v1 = self.parse.match(v1)
		v2 = self.parse.match(v2)

		if not v1 or not v2:
			return False
		for x in [1, 2, 3, 4, 5]:
			one = v1.group(x)
			two = v2.group(x)
			if one == None and two != None:
				return True
			elif one != None and two == None:
				return False
			elif one == None and two == None:
				one = ''
				two = ''
			if one > two:
				return True
			elif one != two:
				return False

	def lt(self, v1, v2):
		return not self.gt(v1, v2)
