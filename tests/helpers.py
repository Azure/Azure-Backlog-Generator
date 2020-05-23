

class Noniterable_str(str):
    def __iter__(self):
        yield self


class StringContains(str):
    def __eq__(self, other):
        return self in other


class Lists():
    @staticmethod
    def contains(list, filter):
        for x in list:
            if filter(x):
                return True
        return False
