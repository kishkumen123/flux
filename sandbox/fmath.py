
import math

def v2lerp(source, dest, f):
    x = source.x + (dest.x - source.x) * f
    y = source.y + (dest.y - source.y) * f

    return v2(x, y)

def v2distance(a, b):
    return abs(math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2)))


class v2():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return "<Vector2 (%s, %s)>" % (self.x, self.y)
