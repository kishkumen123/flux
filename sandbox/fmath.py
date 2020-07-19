
import math

def v2lerp(v1, v2, f):
    x = v1[0] + (v2[0] - v1[0]) * f
    y = v1[1] + (v2[1] - v1[1]) * f

    return Vector2((x, y))

def v2distance(a, b):
    return abs(math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2)))


class Vector2(tuple):
    def __init__(self, values=0):
        if len(values) > 2:
            raise Exception("vector2 can only take tuple of size 2 - %s" % values)
        self.x = values[0]
        self.y = values[1]

    def __getitem__(self, i):
        if i < 0 or i > 1:
            raise Exception("index %s out of range: - %s" % (i, (self.x, self.y)))
        elif i == 0:
            return self.x
        elif i == 1:
            return self.y

    def __repr__(self):
        return "<Vector2 (%s, %s)>" % (self.x, self.y)

    def __str__(self):
        return "<Vector2 (%s, %s)>" % (self.x, self.y)
