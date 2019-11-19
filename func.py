def remap(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def constrain(x, a, b):
    if x < a:
        return a
    elif x > b:
        return b
    else:
        return x


def scale8(i, scale):
    return (i * (1 + scale)) >> 8


def scale8_video(i, scale):
    return ((i * scale) >> 8) + (1 if (i and scale) else 0)
