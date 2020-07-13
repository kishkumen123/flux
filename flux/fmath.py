import math
import pygame


def convert_int_to_rgb(i):
    blue = i & 255
    green = (i >> 8) & 255
    red = (i >> 16) & 255
    return red, green, blue


def convert_rgb_to_int(rgb):
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    i = (red << 16) + (green << 8) + blue
    return i


def translate_range_from_to():
    pass


def convert_num_range(old_range, new_range, old_value):
    new_value = (((old_value - old_range[0]) * (new_range[1] - new_range[0])) / (old_range[1] - old_range[0])) + new_range[0]
    return new_value

def lerp2v(v1, v2, f):
    x = v1[0] + (v2[0] - v1[0]) * f
    y = v1[1] + (v2[1] - v1[1]) * f


    return Vector2((x, y))

def color_lerp(c1, c2, t):
    result = (((t - (-1)) * (1 - 0)) / (1 - (-1))) + 0

    return (
        int((c1[0] + (c2[0] - c1[0]) * result)),
        int((c1[1] + (c2[1] - c1[1]) * result)),
        int((c1[2] + (c2[2] - c1[2]) * result))
    )


def clamp(value, start, end):
    if value < start:
        value = start
    elif value > end:
        value = end

    return value


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

class Vector3(tuple):
    def __init__(self, values=0):
        if len(values) > 3:
            raise Exception("vector2 can only take tuple of size 3 - %s" % values)
        self.x = values[0]
        self.y = values[1]
        self.z = values[2]

    def __getitem__(self, i):
        if i < 0 or i > 2:
            raise Exception("index %s out of range: - %s" % (i, (self.x, self.y, self.z)))
        elif i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z

    def __repr__(self):
        return "<Vector3 (%s, %s, %s)>" % (self.x, self.y, self.z)

    def __str__(self):
        return "<Vector3 (%s, %s, %s)>" % (self.x, self.y, self.z)

class Vector4(tuple):
    def __init__(self, values=0):
        if len(values) > 4:
            raise Exception("vector2 can only take tuple of size 4 - %s" % values)
        self.x = values[0]
        self.y = values[1]
        self.z = values[2]
        self.a = values[3]

    def __getitem__(self, i):
        if i < 0 or i > 3:
            raise Exception("index %s out of range: - %s" % (i, (self.x, self.y, self.z, self.a)))
        elif i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z
        elif i == 3:
            return self.a

    def __repr__(self):
        return "<Vector3 (%s, %s, %s, %s)>" % (self.x, self.y, self.z, self.a)

    def __str__(self):
        return "<Vector3 (%s, %s, %s, %s)>" % (self.x, self.y, self.z, self.a)


def load_image(name, colorkey=None):
    try:
        image = pygame.image.load(name)
    except Exception as e:
        raise e

    image_surface = image.convert()
    return image_surface, image.get_rect()
