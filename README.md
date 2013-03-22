pysemver - Semantic Versioning for Python
=========================================

[![Build Status](https://travis-ci.org/FichteFoll/pysemver.png?branch=master)](https://travis-ci.org/FichteFoll/pysemver)

Usage
=====
Work in progress.

```python
"""pysemver: Semantic Version comparing for Python.

Provides comparing of semantic versions by using SemVer objects using rich comperations plus the
possibility to match a selector string against versions. Interesting for version dependencies.
Versions look like: "1.7.12+b.133"
Selectors look like: ">1.7.0 || 1.6.9+b.111 - 1.6.9+b.113"

Example usage:
    >>> SemVer.valid("1.2.3.4")
    False
    >>> SemVer.clean("this is unimportant text 1.2.3-2 and will be stripped")
    "1.2.3-2"
    >>> SemVer("1.7.12+b.133").satisfies(">1.7.0 || 1.6.9+b.111 - 1.6.9+b.113")
    True
    >>> SemSel(">1.7.0 || 1.6.9+b.111 - 1.6.9+b.113").matches(SemVer("1.7.12+b.133"))
    ["1.7.12+b.133"]

Exported classes:
    * SemVer(object)
        Defines methods for semantic versions.
    * SemSel(object)
        Defines methods for semantic version selectors.
    * SelParseError(Exception)
        An error among others raised when parsing a semantic version selector failed.

Functions:
    none


pysemver Copyright (c) 2013 Zachary King, FichteFoll
This work is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported License. To
view a copy of this license, visit http://creativecommons.org/licenses/by-sa/3.0/.
"""
```

License (MIT)
-------------

    Copyright (c) 2013 Zachary King, FichteFoll

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions: The
    above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.