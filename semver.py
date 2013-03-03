import re


class SemVer(object):

    # Static class variables
    base_regex = (r'([v=]+\s*)?'
                  r'(?P<major>[0-9]+)'
                  r'\.(?P<minor>[0-9]+)'
                  r'\.(?P<patch>[0-9]+)'
                  r'(\-(?P<prerelease>[0-9A-Za-z]+(\.[0-9A-Za-z]+)*))?'
                  r'(\+(?P<build>[0-9A-Za-z]+(\.[0-9A-Za-z]+)*))?')
    search_regex = re.compile(base_regex)
    match_regex  = re.compile('^%s$' % base_regex)

    # Instance variables
    _initialized = False

    # Magic methods
    def __init__(self, version=None, clean=False):
        super(SemVer, self).__init__()

        if version is not None:
            if clean:
                version = self.__class__.clean(version) or version
            self.parse(version)

    def __str__(self):
        temp_str = str(self.major) + "." + str(self.minor) + "." + str(self.patch)
        if self.prerelease is not None:
            temp_str += "-" + str(self.prerelease)
        if self.build is not None:
            temp_str += "+" + str(self.build)
        return temp_str

    def __iter__(self):
        if self._initialized is True:
            result = [self.major,
                    self.minor,
                    self.patch]
            if self.prerelease is not None:
                result.append(self.prerelease)
            if self.build is not None:
                result.append(self.build)
            return iter(result)
        else:
            return False

    def __bool__(self):
        return self._initialized

    # Magic comparing methods
    def __gt__(self, other):
        if isinstance(other, SemVer):
            if self._compare(other) == 1:
                return True
            else:
                return False
        else:
            return NotImplemented

    def __eq__(self, other):
        if isinstance(other, SemVer):
            if self._compare(other) == 0:
                return True
            else:
                return False
        else:
            return NotImplemented

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

    def parse(self, version):
        if not isinstance(version, str):
            raise TypeError("%r is not a string" % version)

        match = self.match_regex.match(version)

        if match is None:
            raise ValueError('%s is not valid SemVer string' % version)

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
        i = 0
        for x1, x2 in zip(self, other):
            if i > 2:
                for y1, y2 in zip(x1.split('.'), x2.split('.')):
                    if y1.isdigit() and y2.isdigit():
                        y1 = int(y1)
                        y2 = int(y2)
                    if y1 > y2:
                        return 1
                    elif y1 < y2:
                        return -1
            else:
                if x1 > x2:
                    return 1
                elif x1 < x2:
                    return -1
            i += 1
        return 0
