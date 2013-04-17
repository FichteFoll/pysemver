pysemver - Semantic Versioning for Python
=========================================

[![Build Status](https://travis-ci.org/FichteFoll/pysemver.png?branch=master)](https://travis-ci.org/FichteFoll/pysemver)

The purpose of this python library is to provide a robust implementation of the
Semantic Versioning methodology. Please review the [Semantic Versioning](http://semver.org)
project page for the details of the spec.


Basic Usage
-----------

The most basic usage of this module is version comparison as follows.

```python
SemVer('1.2.3') < SemVer('2.0.0')
```

To validate version strings, you should use the `valid` method.

```python
SemVer.valid("1.2.3")
```

To extract a version string from inside another string you can use the `clean`
method.

```python
SemVer.clean("this is unimportant text 1.2.3-2 and will be stripped")
# Returns "1.2.3-2"
````

Also, if you are working with dirty strings, you can instantiate the class using
the `SemVer('Extra text 1.2.3', True)` function call. This runs the passed
string through the `SemVer.clean()` method before parsing it.

Advanced Usage
--------------

The previous section introduces the basic usage of the module. For more complex
version checking, such as inside a package manager, the module also provides the
`SemSel` class and the `SemVer.satisfies()` method for sets of conditions.
Internally, `SemVer.satisfies()` calls `SemSel.matches()` so the results are
identical.

### Selectors

The most basic form of selector string is something like `>1.7.0` which will match
version greater than `1.7.0`, this comparison can be done using either of the
following syntaxes.

```python
SemVer('1.8.0').satisfies('>1.7.0')
# Which is equivalent to
bool(SemSel('>1.7.0').matches('1.8.0'))
```

`SemSel.matches()` takes a string, SemVer object, or a mixed list, and then returns a
list of matching versions. If a boolean value is required, it can easily be cast
using the `bool()` method.

Taking this a step further you can define ranges for testing. Say we wanted to
check if a version is greater than `3.0.0` but less than `8.0.0`. This can be done
in two ways, either joining `>3.0.0` and `<8.0.0` with a space (`>3.0.0 <8.0.0`)
or it can be written as a range (`3.0.0 - 8.0.0`). This test can be written as
follows.

```python
SemSel('>3.0.0 <8.0.0').matches('6.0.0')
# Which is equivalent to
SemSel('3.0.0 - 8.0.0').matches('6.0.0')
```

It is also possible to define multiple acceptable patterns for the version. These
patterns are joined using ` || ` as a logical `OR` operator. So if any of the
joined ranges are satisfied, it returns true. For example, if all versions less
than `5.0.0` are acceptable, and versions greater than `8.0.0` are also
acceptable, but the versions in between are not the selector can be written as
follows.

```python
SemSel('<5.0.0 || >8.0.0').matches('9.0.0')
```

### Fuzzy version selection

In addition to the standard comparison operators `< <= = => > !=` it is also
possible to use fuzzy version selection like `~1.0.0` or `1.3.x`. This is useful
for specifying a specific major or minor versions and accepting smaller changes.
For instance `1.2.x` would evaluate to `1.2.0 - 1.2.999999` while `1.x` would
be equal to `1.0.0 - 1.999.999`. The behavior of `~` is similar. `~1.1.2`
evaluates to `1.1.2 - 1.1.999`. 

Please note `999` is just used as a convenient representation for a 'big' number.
These selectors will match up to any value.



TODO: Advanced Advanced `~` operator and `x-ranges`


Classes
-------

* SemVer(object)
	* Defines methods for semantic versions.
	* Immutable and hashable
	* Public methods
		* satisfies(str)
			* returns bool
		* clean(str)
			* returns str
		* valid(str)
			* returns bool
	* Implements rich comparison
* SemSel(object)
	* Defines methods for semantic version selectors.
	* Immutable and hashable
	* Public methods
		* matches(str)
			* returns list of strings
* SelParseError(Exception)
	* An error among others raised when parsing a semantic version selector failed.


Known Issues
------------

* `1.0.0` does not match `1.0.0-beta` or any other pre-release version.


Contributing
------------

We welcome help in making this project better! Please let us know about any bugs
you run in to, and any ideas about how to make it better. We also are glad to
look at pull requests, but be sure to add unittests for new or changed behavior
and that your code passes. Please review the `.travis.yml` file for Python
version and testing environment information.

License (MIT)
-------------

Copyright (c) 2013 Zachary King, FichteFoll

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions: The above copyright notice and this
permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
