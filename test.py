from semver import SemVer

SV = SemVer()


def test(result, test):
	message = " - " + test
	if result:
		print("PASSED" + message)
		return True
	else:
		print("FAILED" + message)
		return False


compare_tests = [
				["0.0.0", "0.0.0food"],
				["0.0.1", "0.0.0"],
				["1.0.0", "0.9.9"],
				["0.10.0", "0.9.0"],
				["0.99.0", "0.10.0"],
				["2.0.0", "1.2.3"],
				["v0.0.0", "0.0.0foo"],
				["v0.0.1", "0.0.0"],
				["v1.0.0", "0.9.9"],
				["v0.10.0", "0.9.0"],
				["v0.99.0", "0.10.0"],
				["v2.0.0", "1.2.3"],
				["0.0.0", "v0.0.0foo"],
				["0.0.1", "v0.0.0"],
				["1.0.0", "v0.9.9"],
				["0.10.0", "v0.9.0"],
				["0.99.0", "v0.10.0"],
				["2.0.0", "v1.2.3"],
				["1.2.3", "1.2.3-asdf"],
				["1.2.3-4", "1.2.3"],
				["1.2.3-4-foo", "1.2.3"],
				["1.2.3-5", "1.2.3-5-foo"],
				["1.2.3-5", "1.2.3-4"],
				["1.2.3-5-foo", "1.2.3-5-Foo"],
				["3.0.0", "2.7.2+"]
			]

i = 0

results = [
			True,
			True,
			True,
			True,
			True,
			True,
			True,
			True,
			True,
			True,
			True,
			True,
			True,
			True,
			True,
			True,
			True,
			True,
			True,
			True,
			True,
			True,
			True,
			True,
			True
			]

print("Starting Compare Tests")

for v in compare_tests:
	print(str(i) + " '" + v[0] + "' and '" + v[1] + "')")
	results[i] = results[i] and test(SV.gt(v[0], v[1]), "gt('" + v[0] + "', '" + v[1] + "')")
	results[i] = results[i] and test(SV.lt(v[1], v[0]), "lt('" + v[1] + "', '" + v[0] + "')")
	results[i] = results[i] and test(not SV.gt(v[1], v[0]), "!gt('" + v[1] + "', '" + v[0] + "')")
	results[i] = results[i] and test(not SV.lt(v[0], v[1]), "!lt('" + v[0] + "', '" + v[1] + "')")
	# results[i] = results[i] and test(SV.eq(v[0], v[0]), "eq('" + v[0] + "', '" + v[0] + "')")
	# results[i] = results[i] and test(SV.eq(v[1], v[1]), "eq('" + v[1] + "', '" + v[1] + "')")
	# results[i] = results[i] and test(SV.neq(v[0], v[1]), "neq('" + v[0] + "', '" + v[1] + "')")
	# results[i] = results[i] and test(SV.cmp(v[1], "==", v[1]), "cmp('" + v[1] + "'' == '" + v[1] + "')")
	# results[i] = results[i] and test(SV.cmp(v[0], ">=", v[1]), "cmp('" + v[0] + "'' >= '" + v[1] + "')")
	# results[i] = results[i] and test(SV.cmp(v[1], "<=", v[0]), "cmp('" + v[1] + "'' <= '" + v[0] + "')")
	# results[i] = results[i] and test(SV.cmp(v[0], "!=", v[1]), "cmp('" + v[1] + "'' != '" + v[1] + "')")
	i += 1

testpass = True
i = 0
for x in results:

	if x:
		print("Test " + str(i) + " - PASSED")
	else:
		print("Test " + str(i) + " - FAILED")

	testpass = testpass and x
	i += 1

if testpass:
	print("Test Group: Compare Tests - PASSED")
else:
	print("Test Group: Compare Tests - FAILED")
