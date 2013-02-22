# class SemVer(object):


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
