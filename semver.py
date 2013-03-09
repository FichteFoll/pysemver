import re
import sys

if sys.version_info[0] == 3:
    basestring = str
    cmp = lambda a, b: (a > b) - (a < b)


# @functools.total_ordering would be nice here but was added in 2.7, __cmp__ is not Py3
class SemVer(object):

    # Static class variables
    base_regex = (r'([v=]+\s*)?'
                  r'(?P<major>[0-9]+)'
                  r'\.(?P<minor>[0-9]+)'
                  r'\.(?P<patch>[0-9]+)'
                  r'(?P<prerelease>\-([0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?)?'
                  r'(?P<build>\+([0-9A-Za-z]+(\.[0-9A-Za-z]+)*)?)?')
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

    # Utility functions
    def satisfies(self, comp_range):
        comp_range = comp_range.replace(" - ", "---")
        or_ranges = comp_range.split(" || ")  # Split sting into segments joined by OR
        or_terms = []
        for x in or_ranges:
            temp = x.split(' ')
            and_terms = []
            for y in temp:
                and_terms.append(y.split('---'))
            or_terms.append(and_terms)

        or_term_truth = False
        for ors in or_terms:
            and_term_truth = True
            for ands in ors:
                and_term_truth = and_term_truth and (self > SemVer(ands[0]) and self < SemVer(ands[1]))
            or_term_truth = or_term_truth or and_term_truth

        return or_term_truth

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

    def _parse(self, version):
        if not isinstance(version, basestring):
            raise TypeError("%r is not a string" % version)

        match = self.match_regex.match(version)

        if match is None:
            raise ValueError('%s is not a valid SemVer string' % version)

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
