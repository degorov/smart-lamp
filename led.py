try:
    from esp import neopixel_write
    from machine import Pin
    LED_PIN = Pin(4, Pin.OUT)
except:
    pass


WIDTH = 10
HEIGHT = 10

MIN_BRIGHTNESS = 16
MAX_BRIGHTNESS = 184


led_map = [[((HEIGHT * (WIDTH - 1)) - HEIGHT * x + y) * 3 if x % 2 else ((HEIGHT * (WIDTH - 1) - 1) - HEIGHT * (x - 1) - y) * 3 for y in range(HEIGHT)] for x in range(WIDTH)]

led_matrix = [ [(0, 0, 0)] * HEIGHT for _ in range(WIDTH) ]

led_buffer = bytearray(HEIGHT * WIDTH * 3)

led_brightness = MAX_BRIGHTNESS


def set_brightness(value):
    global led_brightness
    if value < MIN_BRIGHTNESS:
        led_brightness = MIN_BRIGHTNESS
    elif value > MAX_BRIGHTNESS:
        led_brightness = MAX_BRIGHTNESS
    else:
        led_brightness = value

def adjust_brightness(delta):
    set_brightness(led_brightness + delta * 4)


def scale8(i, scale):
    return (i * (1 + scale)) >> 8

def scale8_video(i, scale):
    return ((i * scale) >> 8) + (1 if (i and scale) else 0)

# inputs are all in range 0-255
# shamelessly ripped from FastLED
def hsv_to_rainbow_rgb(hue, sat, val, cap):

    if cap: val = int(val * led_brightness / 255)

    offset = hue & 0x1F
    offset8 = offset << 3
    third = scale8(offset8, 85)

    if not(hue & 0x80):
        if not(hue & 0x40):
            if not(hue & 0x20):
                r = 255 - third
                g = third
                b = 0
            else:
                r = 171
                g = 85 + third
                b = 0
        else:
            if not(hue & 0x20):
                twothirds = scale8(offset8, 170)
                r = 171 - twothirds
                g = 170 + third
                b = 0
            else:
                r = 0
                g = 255 - third
                b = third
    else:
        if not(hue & 0x40):
            if not(hue & 0x20):
                r = 0
                twothirds = scale8(offset8, 170)
                g = 171 - twothirds
                b = 85 + twothirds
            else:
                r = third
                g = 0
                b = 255 - third
        else:
            if not(hue & 0x20):
                r = 85 + third
                g = 0
                b = 171 - third
            else:
                r = 170 + third
                g = 0
                b = 85 - third

    if sat != 255:
        if sat == 0:
            r = 255
            b = 255
            g = 255
        else:
            if r: r = scale8(r, sat)
            if g: g = scale8(g, sat)
            if b: b = scale8(b, sat)
            desat = 255 - sat
            desat = scale8(desat, desat)
            brightness_floor = desat
            r = r + brightness_floor
            g = g + brightness_floor
            b = b + brightness_floor

    if val != 255:
        val = scale8_video(val, val)
        if val == 0:
            r = 0
            g = 0
            b = 0
        else:
            if r: r = scale8(r, val)
            if g: g = scale8(g, val)
            if b: b = scale8(b, val)

    return r, g, b


def fill_solid(h, s, v):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            led_matrix[x][y] = (h, s, v)


def render(cap):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            idx = led_map[x][y]
            led_buffer[idx + 1], led_buffer[idx], led_buffer[idx + 2] = hsv_to_rainbow_rgb(led_matrix[x][y][0], led_matrix[x][y][1], led_matrix[x][y][2], cap)
    neopixel_write(LED_PIN, led_buffer, 1)


def loading_rings(progress):
    rings = progress * HEIGHT // 100
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if y <= rings - 1:
                led_matrix[x][y] = (int(y * 256 / HEIGHT), 255, 255)
            else:
                led_matrix[x][y] = (0, 0, 0)
    render(True)
