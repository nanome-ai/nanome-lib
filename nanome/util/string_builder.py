class StringBuilder:
    def __init__(self):
        self.los =[]

    def append(self, s):
        self.los.append(str(s))

    def to_string(self):
        joined = "".join(self.los)
        self.los = [joined]
        return joined

    def clear(self):
        del self.los[:]