import math

class Vector3(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def get_copy(self):
        return Vector3(self.x, self.y, self.z)

    @classmethod
    def distance(cls, v1, v2):
        return math.sqrt((v2.x - v1.x) ** 2 + (v2.y - v1.y) ** 2 + (v2.z - v1.z) ** 2)

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def unpack (self):
        return self.x, self.y, self.z