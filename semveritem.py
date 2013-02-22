import re


class SemVerItem(object):

    regex = re.compile(r'^(?P<major>[0-9]+)'
                    r'\.(?P<minor>[0-9]+)'
                    r'\.(?P<patch>[0-9]+)'
                    r'(\-(?P<prerelease>[0-9A-Za-z]+(\.[0-9A-Za-z]+)*))?'
                    r'(\+(?P<build>[0-9A-Za-z]+(\.[0-9A-Za-z]+)*))?$')

    # Core methods

    def __init__(self, version):
        if version == None:
            self.initialized = False
            raise TypeError("There was no value passed to SemVerItem __init__ "
                            "method.")
        else:
            ver_type = type(version)
            if ver_type == "str":
                self.parse(version)
            elif isinstance(version, SemVerItem):
                self = version
            elif ver_type == type([0, 0]) or ver_type == type((0, 0)):
                if len(version) >= 3:
                    self._set_from_iter(version)
                else:
                    raise TypeError
            else:
                raise TypeError("Value passed to SemVerItem __init__ method"
                                "was not a string, list, tuple, or instance")
            self.initialized = True

    def __bool__(self):
        return self.initialized

    def __lt__(self, other):
        pass

    def __le__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __str__(self):
        temp_str = self.major + "." + self.minor + "." + self.patch
        if self.prerelease != None:
            temp_str += "-" + self.prerelease
        if self.build != None:
            temp_str += "+" + self.build
        return temp_str

    def __iter__(self):
        if self.initialized == True:
            return [self.major,
                    self.minor,
                    self.patch,
                    self.prerelease,
                    self.build]
        else:
            return False

    # Utility functions

    def get_array(self):
        data = [self.major, self.minor, self.patch]
        if self.prerelease != None:
            data.append(self.prerelease)
        if self.build != None:
            data.append(self.build)
        return data

    def _set_from_iter(self, items):
        self.major, self.minor, self.patch, self.prerelease, self.build = items

    def parse(self, version):
        match = self.regex.match(version)

        if match is None:
            raise ValueError('% is not valid SemVer string' % version)

        info = match.groupdict()

        self.major = int(info['major'])
        self.minor = int(info['minor'])
        self.patch = int(info['patch'])

        if info['prerelease'] != None:
            self.prerelease = info['prerelease']
        else:
            self.prerelease = 0
        if info['build'] != None:
            self.build = info['build']
        else:
            self.build = 0
        return True

    def _compare_by_keys(self, other):
        for x1, x2 in zip(self, other):
            if x1 > x2:
                return 1
            elif x1 < x2:
                return -1
        if len(x1) > len(x2):
            return 1
        elif len(x1) < len(x2):
            return -1
        else:
            return 0
