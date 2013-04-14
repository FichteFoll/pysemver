pysemver - Semantic Versioning for Python
=========================================

[![Build Status](https://travis-ci.org/FichteFoll/pysemver.png?branch=master)](https://travis-ci.org/FichteFoll/pysemver)

The purpose of this python library is to provide a robust implementation of the
Semantic Versioning methodology. Please review the [Semantic Versioning](http://semver.org)
project page for information about the details about how it works.


Usage
=====

The most basic usage of this module is basic version comparison as follows.

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

All of this functionality is great, but the most useful application for this
module is when you use the `SemVer.satisfies()` or `SemSel.matches()` functions.

The `satisfies` method is used on a SemVer object. The parameter for the method
is a string defining a versions that should be tested for. If you wanted to
build a selector for greater than `1.7.0` it would be `>1.7.0`. For a range of
versions (between 1.7.0 and 2.0.0) is could be defined as either `1.7.0 - 2.0.0`
or `>=1.7.0 <=2.0.0`. Spaces (` `) are treated as `AND` joining terms together

```python
SemVer("1.9.0").satisfies(">1.8.0")

SemVer("1.9.0").satisfies(">1.8.0 <2.0.0")

SemVer("1.9.0").satisfies("1.8.0 - 2.0.0")
```

The previous statements can be rewritten as follows.

```python
SemSel(">1.8.0").matches("1.9.0")

SemSel(">1.8.0 <2.0.0").matches("1.9.0")

SemSel("1.8.0 - 2.0.0").matches("1.9.0")
```

You can define multiple conditions for evaulation using `||` as `OR` like like
this `1.8.0 - 2.0.0 || 3.0.0 - 5.0.0`, or written in code like as follows.

```python
SemSel("1.8.0 - 2.0.0 || 3.0.0 - 5.0.0").matches("1.9.0")
SemSel("1.8.0 - 2.0.0 || 3.0.0 - 5.0.0").matches("4.0.0")

SemVer("1.9.0").satisfies("1.8.0 - 2.0.0 || 3.0.0 - 5.0.0")
SemVer("4.0.0").satisfies("1.8.0 - 2.0.0 || 3.0.0 - 5.0.0")
```


Classes
=======

### SemVer(object)
    
Defines methods for semantic versions.


### SemSel(object)

Defines methods for semantic version selectors.


### SelParseError(Exception)

An error among others raised when parsing a semantic version selector failed.


Contributing
============

We welcome help in making this project better! Please let us know about any bugs
you run in to, and any ideas about how to make it better. We also are glad to
look at pull requests, but you must write unittests for your code, and it must
work in both python 2 and 3.

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
