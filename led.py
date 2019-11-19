import machine
import esp
import func


LED_PIN = machine.Pin(4, machine.Pin.OUT)

WIDTH = 8
HEIGHT = 10


led_map = [[((HEIGHT * (WIDTH - 1)) - HEIGHT * x + y) * 3 if x % 2 else ((HEIGHT * (WIDTH - 1) - 1) - HEIGHT * (x - 1) - y) * 3 for y in range(HEIGHT)] for x in range(WIDTH)]

led_matrix = [ [(0, 0, 0)] * HEIGHT for _ in range(WIDTH) ]

led_buffer = bytearray(HEIGHT * WIDTH * 3)


# inputs are all in range 0-255
# shamelessly ripped from FastLED
def hsv_to_rainbow_rgb(hue, sat, val):

    offset = hue & 0x1F
    offset8 = offset << 3
    third = func.scale8(offset8, 85)

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
                twothirds = func.scale8(offset8, 170)
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
                twothirds = func.scale8(offset8, 170)
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
            if r: r = func.scale8(r, sat)
            if g: g = func.scale8(g, sat)
            if b: b = func.scale8(b, sat)
            desat = 255 - sat
            desat = func.scale8(desat, desat)
            brightness_floor = desat
            r = r + brightness_floor
            g = g + brightness_floor
            b = b + brightness_floor

    if val != 255:
        val = func.scale8_video(val, val)
        if val == 0:
            r = 0
            g = 0
            b = 0
        else:
            if r: r = func.scale8(r, val)
            if g: g = func.scale8(g, val)
            if b: b = func.scale8(b, val)

    return r, g, b


def fill_solid(h, s, v):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            led_matrix[x][y] = (h, s, v)


def render():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            idx = led_map[x][y]
            led_buffer[idx + 1], led_buffer[idx], led_buffer[idx + 2] = hsv_to_rainbow_rgb(*led_matrix[x][y])
    esp.neopixel_write(LED_PIN, led_buffer, 1)
