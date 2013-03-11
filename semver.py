import re
import sys


__all__ = ['SemVer', 'SemSel', 'SelParseError']

if sys.version_info[0] == 3:
    basestring = str
    cmp = lambda a, b: (a > b) - (a < b)


# @functools.total_ordering would be nice here but was added in 2.7, __cmp__ is not Py3
class SemVer(object):

    # Static class variables
    base_regex = r'''(?x)([v=]+)?
        (?P<major>[0-9]+)
        \.(?P<minor>[0-9]+)
        \.(?P<patch>[0-9]+)
        (?P<prerelease>\-([0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?)?
        (?P<build>\+([0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?)?'''
    search_regex = re.compile(base_regex)
    match_regex  = re.compile('^%s$' % base_regex)  # required because of $ anchor

    # Magic methods
    def __init__(self, version, clean=False):
        super(SemVer, self).__init__()

        if clean:
            version = self.__class__.clean(version) or version
        self._parse(version)

    def __str__(self):
        return "{0}.{1}.{2}{3}{4}".format(*list(self))

    def __repr__(self):
        return 'SemVer("%s")' % self

    def __iter__(self):
        if self._initialized is False:
            return False

        result = [self.major,
                  self.minor,
                  self.patch,
                  self.prerelease or "",
                  self.build or ""]
        return iter(result)

    def __hash__(self):
        return hash(str(self))

    # Magic comparing methods
    def __gt__(self, other):
        return self._compare(other) == 1 if isinstance(other, SemVer) else NotImplemented

    def __eq__(self, other):
        return self._compare(other) == 0 if isinstance(other, SemVer) else NotImplemented

    def __lt__(self, other):
        return not (self > other or self == other)

    def __ge__(self, other):
        return not (self < other)

    def __le__(self, other):
        return not (self > other)

    def __ne__(self, other):
        return not (self == other)

    # Utility methods
    def satisfies(self, sel):
        if not isinstance(sel, SemSel):
            sel = SemSel(sel)  # just "re-raise" exceptions

        return bool(sel.matches(self))

    @classmethod
    def valid(cls, version):
        if not isinstance(version, basestring):
            raise TypeError("%r is not a string" % version)

        if cls.match_regex.match(version):
            return True
        else:
            return False

    @classmethod
    def clean(cls, version):
        m = cls.search_regex.search(version)
        if m:
            return version[m.start():m.end()]
        else:
            return None

    # Private methods
    def _parse(self, version):
        if not isinstance(version, basestring):
            raise TypeError("%r is not a string" % version)

        match = self.match_regex.match(version)

        if match is None:
            raise ValueError("'%s' is not a valid SemVer string" % version)

        info = match.groupdict()

        self.major = int(info['major'])
        self.minor = int(info['minor'])
        self.patch = int(info['patch'])

        if info['prerelease'] is not None:
            self.prerelease = info['prerelease']
        else:
            self.prerelease = None
        if info['build'] is not None:
            self.build = info['build']
        else:
            self.build = None

        self._initialized = True
        return True

    def _compare(self, other):
        # Shorthand lambdas
        cp_len = lambda t, i=0: cmp(len(t[i]), len(t[not i]))
        one_is_not = lambda a, b: (not a and b) or (not b and a)

        i = 0
        t1 = [tuple(self), tuple(other)]
        for x1, x2 in zip(*t1):
            if i > 2:
                # self is greater when other has a prerelease but self doesn't
                # self is less    when other has a build      but self doesn't
                if one_is_not(x1, x2):
                    return 2 * (i - 3.5) * (1 - 2 * bool(x2))

                # Remove leading '-' and '+'
                x1, x2 = x1[1:], x2[1:]

                # self is less when other's build is only '+'
                if i == 4 and one_is_not(x1, x2):
                    return 1 - 2 * bool(x1)

                # Split by '.' and use numeric comp or lexicographical order
                t2 = [x1.split('.'), x2.split('.')]
                for y1, y2 in zip(*t2):
                    if y1.isdigit() and y2.isdigit():
                        y1 = int(y1)
                        y2 = int(y2)
                    if y1 > y2:
                        return 1
                    elif y1 < y2:
                        return -1

                # The "longer" sub-version is greater
                d = cp_len(t2)
                if d:
                    return d
            else:
                if x1 > x2:
                    return 1
                elif x1 < x2:
                    return -1
            i += 1

        # The versions equal
        return 0


class SemComperator(object):
    """SemComperator('<=', SemVer("1.2.3"))
    """
    ops = {
        '>=': '__ge__',
        '<=': '__le__',
        '>':  '__gt__',
        '<':  '__lt__',
        '=':  '__eq__',
        '!=': '__ne__'
    }

    def __init__(self, op, ver):
        super(SemComperator, self).__init__()
        self.op  = op or '='
        self.ver = ver

    def matches(self, ver):
        # TODO
        return getattr(ver, self.ops[self.op])(self.ver)

    def __str__(self):
        return (self.op or "") + str(self.ver)


class SemSelAndChunk(list):
    def matches(self, ver):
        return all(cp.matches(ver) for cp in self)

    def __str__(self):
        return ' '.join(map(str, self))

    def add_child(self, op, ver):
        self.append(SemComperator(op, SemVer(ver)))


class SemSelOrChunk(list):
    def matches(self, ver):
        return any(ch.matches(ver) for ch in self)

    def __str__(self):
        return ' || '.join(map(str, self))

    def new_child(self):
        ch = SemSelAndChunk()
        self.append(ch)
        return ch


class SelParseError(Exception):
    pass


class SemSel(object):
    """Short for "Semantic Version Selector" or whatever.
    """
    fuzzy_regex = re.compile(r'''(?x)^
        (?P<op>[<>]=?|!=|~>?=?)?
        (?:[v=]*(?P<major>\d+)
         (?:\.(?P<minor>\d+)
          (?:\.(?P<patch>\d+)
           (?P<other>[-+][a-zA-Z0-9-+.]*)?
          )?
         )?
        )?$''')
    xrange_regex = re.compile(r'''(?x)^
        (?P<op>[<>]=?|!=|~>?=?)?
        (?:[v=]*(?P<major>\d+|[xX*])
         (?:\.(?P<minor>\d+|[xX*])
          (?:\.(?P<patch>\d+|[xX*]))?
         )?
        )
        (?P<other>.*)$''')
    split_op_regex = re.compile(r'^(?P<op>[<>!]?=|<|>)?(?P<ver>.*)$')

    def __init__(self, sel):
        super(SemSel, self).__init__()

        self.chunk = SemSelOrChunk()
        self._parse(sel)

    # Magic methods
    def __str__(self):
        return str(self.chunk)

    def __repr__(self):
        return 'SemSel("%s")' % self.chunk

    def __hash__(self):
        return hash(str(self))

    # Utility methods
    def matches(self, *vers):
        ret = []
        for v in vers:
            if self.chunk.matches(v):
                ret.append(v)

        return ret or False

    # Private methods
    def _parse(self, sel):
        """ 1. split by whitespace into tokens
                a. start new and_chunk on ' || '
                b. parse " - " ranges
                c. replace "xX*" ranges with "~" equivalent
                d. parse "~" ranges
                e. parse unmatched token as comperator
                ~. append to current and_chunk
            2. store in self.chunk

            Raises TypeError, ValueError or SelParseError.
        """
        if not isinstance(sel, basestring):
            raise TypeError("Selector must be a string")

        # Split selector by spaces and crawl the tokens
        tokens = sel.split()
        i = -1
        and_chunk = self.chunk.new_child()

        while i + 1 < len(tokens):
            i += 1
            t, tt = (tokens[i],) * 2

            # Replace x ranges with ~ selector
            m = self.xrange_regex.match(t)
            m = m and m.groups('')
            if m and any(x in 'xX*' for x in m[1:4]) and not m[0].startswith('>'):
                # Remove any ".x" and append "~" if not already present (do not match '>1.0' or '>*')
                t = m[0] + '.'.join(x for x in m[1:4] if x.isdigit()) + m[4]
                if not t.startswith('~'):
                    t = '~' + t

            if t == '||':
                # Start a new and_chunk, don't care about consecutive ORs
                and_chunk = self.chunk.new_child()

            elif t == '-':
                # ' - ' range
                i += 1
                t = tokens[i]
                c = and_chunk[-1]  # If this results in an exception you know you're doing it wrong

                if c.op != '=' or len(tokens) < i + 1:
                    raise SelParseError("Invalid ' - ' range '%s - %s'" % (c.ver, tt))
                c.op = ">="
                and_chunk.add_child('<=', t)

            elif t == '':
                # Multiple spaces
                pass

            elif t.startswith('~'):
                m = self.fuzzy_regex.match(t)
                if not m:
                    raise SelParseError("Invalid fuzzy range or XRange '%s'" % tt)

                mm, m = m.groups('')[1:4], m.groupdict('')  # mm: major to patch
                if m['other']:
                    raise SelParseError("XRanges do not allow pre-release or build tags")

                the_op = ['>=', '<']
                # Reverse ops if '~!'
                if '!' in m['op']:
                    the_op.reverse()
                # Minimum requirement
                and_chunk.add_child(the_op[0], '.'.join(x or '0' for x in mm) + '-')

                if m['major']:
                    # Increase version before none (or second to last if '~1.2.3')
                    e = [0, 0, 0]
                    for j, d in enumerate(mm):
                        if not d or j == len(mm) - 1:
                            e[j - 1] = e[j - 1] + 1
                            break
                        e[j] = int(d)

                    and_chunk.add_child(the_op[1], '.'.join(str(x) for x in e) + '-')

                # else: just plain '~' or '*', or '~>X', already handled

            else:
                # A normal comperator
                m = self.split_op_regex.match(t).groupdict()  # this regex can't fail
                and_chunk.add_child(**m)
