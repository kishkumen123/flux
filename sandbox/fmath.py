
import math

def v2lerp(source, dest, f):
    x = source.x + (dest.x - source.x) * f
    y = source.y + (dest.y - source.y) * f

    return v2(x, y)

def v2distance(a, b):
    return abs(math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2)))


#TODO(Rafik): item assignment __setitem__ or something else so that you can do position[0] = 1
class v2():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __getitem__(self, i):
        if i==0: return self.x
        if i==1: return self.y
        raise Exception("index %s out of bounds. %s)" % (i, self))

    def __repr__(self):
        return "<Vector2 (%s, %s)>" % (self.x, self.y)

class v4():
    def __init__(self, x=0, y=0, z=0, w=0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __getitem__(self, i):
        if i==0: return self.x
        if i==1: return self.y
        if i==2: return self.z
        if i==3: return self.w
        raise Exception("index %s out of bounds. %s)" % (i, self))

    def __repr__(self):
        return "<Vector2 (%s, %s, %s, %s)>" % (self.x, self.y, self.z, self.w)


#TODO(Rafik): MAKE A FUCKING CLAMP METHOD
def clamp(): pass

