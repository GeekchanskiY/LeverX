from functools import total_ordering

class Version:
    def __init__(self, version):
        self.normalized_version = self.normalize(version)

    def normalize(self, version):
        args_to_replace = {
            '-': '',
            'alpha': '.1',
            'beta': '.2',
            'b': '.2',
            'rc': '.3'
        }
        version_str = version
        for key in args_to_replace.keys():
            version_str = version_str.replace(key, args_to_replace[key])
        version_list = version_str.split('.')

        # Данный луп нужен для избежания ситуаций 1.0.0.0 != 1.0.0
        while True:
            if version_list[-1] == "0" and len(version_list) > 3:
                del version_list[-1]
            else: break


        while True:
            if len(version_list) > 2:
                return version_list
            else: version_list.append('0')


    def __lt__(self, other):
        for my_ver, other_ver in zip(self.normalized_version, other.normalized_version):
            if my_ver < other_ver: return True
            elif my_ver > other_ver: return False
        return True if len(self.normalized_version) > len(other.normalized_version) else False


    def __eq__(self, other):
        if len(self.normalized_version) == len(other.normalized_version):
            for my_version,other_version in zip(self.normalized_version, other.normalized_version):
                if my_version != other_version: return False
        else:
            return False
        return True


def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0")
    ]

    for version_1, version_2 in to_test:
        print(version_1,version_2)
        assert Version(version_1) < Version(version_2), "le failed"
        assert Version(version_2) > Version(version_1), "ge failed"
        assert Version(version_2) != Version(version_1), "neq failed"

    #assert Version("1") == Version("1.0.0.0.0"), "fiasco"

if __name__ == "__main__":
    main()