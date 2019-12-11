import math


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

