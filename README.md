pysemver - Semantic Versioning for Python
=========================================

[![Build Status](https://travis-ci.org/FichteFoll/pysemver.png?branch=master)](https://travis-ci.org/FichteFoll/pysemver)

The purpose of this python library is to provide a fully compliant implementation
of the Semantic Versioning methodology. Please review the [Semantic Versioning](http://semver.org) project page for the details of the spec.

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
```

Alternatively, setting the second parameter to true will trigger this action
before instantiating the object. `SemVer('Extra text 1.2.3', True)`


Selectors
---------

PySemVer utualizes selectors as specified in the SemVer spec.

* `||` is a logical **OR**
* **SPACE** is a logical **AND**
* ` - ` specifies a range
* Comparison Operators perform as expected
	* `< <= => > !=`
* Examples of valid selectors
	* `>1.7.0`
	* `>3.0.0 <8.0.0` = `3.0.0 - 8.0.0`
	* `<5.0.0 || >8.0.0`


Comparison Functions
--------------------

PySemVer supplies two methods for using the selectors

* `SemVer.satisfies()`
	* Returns a boolean value
	* Usage `SemVer('1.0.0').satisfies('>0.6.0')`
* `SemSel.matches()`
	* Returns a list of matching versions
	* Usage `SemSel('>1.7.0').matches('1.9.0')` returns `1.9.0` or
	* `SemSel('>1.7.0').matches('1.6.0', '1.9.0', '2.0.0')` returns `['1.9.0', '2.0.0']`


Fuzzy Version Selectors
-----------------------

In addition to the previous selectors, PySemVer also supports
fuzzy selectors and x-ranges.

* `~` can be used like `~1` or `~1.0`, matching `1.0.0 - 1.9999.9999` and `1.0.0 - 1.0.9999` respectively 
* `x` can be used as a wild card character like `1.0.x` which matches `1.0.0 - 1.0.9999`


Classes
-------

* SemVer
	* Defines methods for semantic versions.
	* Implements rich comparison
	* Immutable and hashable
* SemSel
	* Defines methods for semantic version selectors.
	* Immutable and hashable
* SelParseError
	* Defines error throw for failed parsing of selector

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
