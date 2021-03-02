try:
    import uos
    import urandom
    from utime import sleep_ms, localtime
except:
    import os as uos
    import random as urandom
    import time
    def sleep_ms(n):
        time.sleep(n / 1000)
    def localtime():
        return time.localtime()
    import types
    micropython = types.SimpleNamespace()
    def native(f, *args, **kwargs):
        def dummy(*args, **kwargs):
            return f(*args, **kwargs)
        return dummy
    micropython.native = native

import led
import math


@micropython.native
def constrain(x, a, b):
    if x < a:
        return a
    elif x > b:
        return b
    else:
        return x


current_effect_idx = 3
current_effect = None


def next_effect(switch):

    global current_effect, current_effect_idx

    led.fill_solid(0, 0, 0)

    if switch:
        if current_effect_idx == 10:
            current_effect_idx = 0
        else:
            current_effect_idx += 1

    if current_effect_idx == 0:
        current_effect = Void()
    elif current_effect_idx == 1:
        current_effect = SelectedColor()
    elif current_effect_idx == 2:
        current_effect = AllHueLoop(192)
    elif current_effect_idx == 3:
        current_effect = VerticalRainbow(2)
    elif current_effect_idx == 4:
        current_effect = HorizontalRainbow(2)
    elif current_effect_idx == 5:
        current_effect = Matrix(40, 20)
    elif current_effect_idx == 6:
        current_effect = Sparkles(2, 8)
    elif current_effect_idx == 7:
        current_effect = Lighters(5, 8)
    elif current_effect_idx == 8:
        current_effect = Plasma(0.1)
    elif current_effect_idx == 9:
        current_effect = Fire(0)
    elif current_effect_idx == 10:
        current_effect = Clock(34)

# ============================================================================ #

class Void:

    @micropython.native
    def update(self):
        led.fill_solid(0, 0, 0)

    def adjust(self, delta):
        pass

    def value(self, state):
        pass

    def getvalue(self):
        return 0

# ============================================================================ #

class SelectedColor:

    def __init__(self):
        self.hue = 0
        self.sat = 255

    @micropython.native
    def update(self):
        led.fill_solid(self.hue, self.sat, 255)

    def adjust(self, delta):
        self.hue = (self.hue + delta) % 256
        self.sat = 255

    def value(self, state):
        self.hue = state // 256
        self.sat = state % 256

    def getvalue(self):
        return self.hue * 256 + self.sat

# ============================================================================ #

class AllHueLoop:

    def __init__(self, sat):
        self.hue = 0
        self.sat = 192

    @micropython.native
    def update(self):

        led.fill_solid(self.hue, self.sat, 255)

        if self.hue == 256:
            self.hue = 0
        else:
            self.hue += 1

    def adjust(self, delta):
        self.sat = constrain(self.sat + delta, 0, 255)

    def value(self, state):
        self.sat = state

    def getvalue(self):
        return self.sat

# ============================================================================ #

class VerticalRainbow:

    def __init__(self, speed):
        self.position = 0
        self.speed = speed

    @micropython.native
    def update(self):
        self.position = (self.position + self.speed) % 256
        for x in range(led.WIDTH):
            for y in range(led.HEIGHT):
                led.led_matrix[x][y] = (int(y * 256 / led.HEIGHT) - self.position, 255, 255)

    def adjust(self, delta):
        self.speed = constrain(self.speed + delta, -8, 8)

    def value(self, state):
        self.speed = state - 8

    def getvalue(self):
        return self.speed + 8

# ============================================================================ #

class HorizontalRainbow:

    def __init__(self, speed):
        self.position = 0
        self.speed = speed

    @micropython.native
    def update(self):
        self.position = (self.position + self.speed) % 256
        for x in range(led.WIDTH):
            for y in range(led.HEIGHT):
                led.led_matrix[x][y] = (int(x * 256 / led.WIDTH) - self.position, 255, 255)

    def adjust(self, delta):
        self.speed = constrain(self.speed + delta, -8, 8)

    def value(self, state):
        self.speed = state - 8

    def getvalue(self):
        return self.speed + 8

# ============================================================================ #

class Matrix:

    def __init__(self, scale, step):
        self.scale = scale
        self.step = step

    @micropython.native
    def update(self):

        sleep_ms(30)

        for x in range(led.WIDTH):
            this_color_v = led.led_matrix[x][led.HEIGHT - 1][2]
            if this_color_v == 0:
                led.led_matrix[x][led.HEIGHT - 1] = (96, 255, 255 * (urandom.randrange(self.scale) == 0))
            elif this_color_v < self.step:
                led.led_matrix[x][led.HEIGHT - 1] = (0, 0, 0)
            else:
                led.led_matrix[x][led.HEIGHT - 1] = (96, 255, this_color_v - self.step)

        for x in range(led.WIDTH):
            for y in range(led.HEIGHT - 1):
                led.led_matrix[x][y] = led.led_matrix[x][y + 1]

    def adjust(self, delta):
        self.scale = constrain(self.scale - delta * 5, 5, 150)

    def value(self, state):
        self.scale = state

    def getvalue(self):
        return -self.scale

# ============================================================================ #

class Sparkles:

    def __init__(self, scale, step):
        self.scale = scale
        self.step = step

    @micropython.native
    def update(self):

        for i in range(self.scale):
            x = urandom.randrange(led.WIDTH)
            y = urandom.randrange(led.HEIGHT)
            if led.led_matrix[x][y][2] == 0:
                led.led_matrix[x][y] = (ord(uos.urandom(1)), 255, 255)

        for x in range(led.WIDTH):
            for y in range(led.HEIGHT):
                this_color = led.led_matrix[x][y]
                if this_color[2] > self.step:
                    led.led_matrix[x][y] = (this_color[0], this_color[1], this_color[2] - self.step)
                else:
                    led.led_matrix[x][y] = (0, 0, 0)

    def adjust(self, delta):
        self.scale = constrain(self.scale + delta, 1, 32)

    def value(self, state):
        self.scale = state

    def getvalue(self):
        return self.scale

# ============================================================================ #

class Lighters:

    def __init__(self, number, freq):

        self.loading_flag = True

        self.number = number
        self.freq = freq

        self.lighters_pos = [ [0] * 16 for _ in range(2) ]
        self.lighters_speed = [ [0] * 16 for _ in range(2) ]
        self.lighters_color = [(0, 0, 0)] * 16
        self.loop_counter = 0


    @micropython.native
    def update(self):

        if self.loading_flag:
            self.loading_flag = False
            for i in range(self.number):
                self.lighters_pos[0][i] = urandom.randrange(led.WIDTH * 10)
                self.lighters_pos[1][i] = urandom.randrange(led.HEIGHT * 10)
                self.lighters_speed[0][i] = urandom.randrange(-5, 6)
                self.lighters_speed[1][i] = urandom.randrange(-6, 6)
                self.lighters_color[i] = (ord(uos.urandom(1)), 255, 255)

        led.fill_solid(0, 0, 0)

        self.loop_counter = (self.loop_counter + 1) % self.freq

        for i in range(self.number):

            if self.loop_counter == 0:
                self.lighters_speed[0][i] = self.lighters_speed[0][i] + urandom.randrange(-1, 2)
                self.lighters_speed[1][i] = self.lighters_speed[1][i] + urandom.randrange(-1, 2)
                self.lighters_speed[0][i] = constrain(self.lighters_speed[0][i], -10, 10)
                self.lighters_speed[1][i] = constrain(self.lighters_speed[1][i], -10, 10)

            self.lighters_pos[0][i] = self.lighters_pos[0][i] + self.lighters_speed[0][i]
            self.lighters_pos[1][i] = self.lighters_pos[1][i] + self.lighters_speed[1][i]

            if self.lighters_pos[0][i] < 0:
                self.lighters_pos[0][i] = (led.WIDTH - 1) * 10

            if self.lighters_pos[0][i] >= led.WIDTH * 10:
                self.lighters_pos[0][i] = 0

            if self.lighters_pos[1][i] < 0:
                self.lighters_pos[1][i] = 0
                self.lighters_speed[1][i] = -self.lighters_speed[1][i]

            if self.lighters_pos[1][i] >= (led.HEIGHT - 1) * 10:
                self.lighters_pos[1][i] = (led.HEIGHT - 1) * 10
                self.lighters_speed[1][i] = -self.lighters_speed[1][i]

            led.led_matrix[self.lighters_pos[0][i] // 10][self.lighters_pos[1][i] // 10] = self.lighters_color[i]


    def adjust(self, delta):
        self.number = constrain(self.number + delta, 1, 16)

    def value(self, state):
        self.number = state

    def getvalue(self):
        return self.number

# ============================================================================ #

class Plasma:

    def __init__(self, speed):
        self.speed = speed
        self.counter = 0

    @micropython.native
    def update(self):

        self.counter = self.counter + self.speed

        for x in range(led.WIDTH):
            for y in range(led.HEIGHT):
                hue = int((
                    math.sin( self.counter + x ) +
                    math.sin( self.counter + y / 4.5 ) +
                    math.sin( x + y + self.counter ) +
                    math.sin( math.sqrt( ( x + self.counter ) ** 2.0 + ( y + 1.5 * self.counter ) ** 2.0 ) / 4.0 )
                    + 4) * 32)
                led.led_matrix[x][y] = (hue, 255, 255)

    def adjust(self, delta):
        self.speed = constrain(self.speed + delta / 100, 0.05, 0.5)

    def value(self, state):
        self.speed = state / 100

    def getvalue(self):
        return int(self.speed * 100)

# ============================================================================ #

fire_value_mask = ((0  , 0  , 0  , 0 , 0 , 0  , 0  , 0  , 32 , 32 ),
                   (0  , 0  , 0  , 0 , 0 , 0  , 0  , 0  , 64 , 64 ),
                   (32 , 0  , 0  , 0 , 0 , 0  , 0  , 32 , 96 , 96 ),
                   (64 , 32 , 0  , 0 , 0 , 0  , 32 , 64 , 128, 128),
                   (96 , 64 , 32 , 0 , 0 , 32 , 64 , 96 , 160, 160),
                   (128, 96 , 64 , 32, 32, 64 , 96 , 128, 192, 192),
                   (160, 128, 96 , 64, 64, 96 , 128, 160, 255, 255),
                   (192, 160, 128, 96, 96, 128, 160, 192, 255, 255))

fire_hue_mask = ((11, 19, 22, 25, 25, 22, 19, 11, 1 , 1),
                 (8 , 13, 19, 22, 22, 19, 13, 8 , 1 , 1),
                 (8 , 13, 16, 19, 19, 16, 13, 8 , 1 , 1),
                 (5 , 11, 13, 16, 16, 13, 11, 5 , 1 , 1),
                 (5 , 11, 11, 13, 13, 11, 11, 5 , 1 , 1),
                 (1 , 5 , 8 , 11, 11, 8 , 5 , 1 , 0 , 0),
                 (0 , 1 , 5 , 8 , 8 , 5 , 1 , 0 , 0 , 0),
                 (0 , 0 , 1 , 5 , 5 , 1 , 0 , 0 , 0 , 0))


class Fire:

    def __init__(self, hue):

        self.loading_flag = True

        self.hue = hue

        self.line = [0] * led.WIDTH
        self.pcnt = 0

        self.matrix_value = [ [0] * 10 for _ in range(8) ]


    @micropython.native
    def generate_line(self):
        for x in range(led.WIDTH):
            self.line[x] = urandom.randrange(64, 256)


    @micropython.native
    def update(self):

        if self.loading_flag:
            self.loading_flag = False
            self.generate_line()

        if self.pcnt >= 100:

            for y in range(led.HEIGHT - 1, 0, -1):
                for x in range(led.WIDTH):
                    if y <= 7:
                        self.matrix_value[y][x] = self.matrix_value[y - 1][x]

            for x in range(led.WIDTH):
                self.matrix_value[0][x] = self.line[x]

            self.generate_line()
            self.pcnt = 0

        for y in range(7, 0, -1):
            for x in range(0, led.WIDTH):
                led.led_matrix[x][y] = (int(self.hue + fire_hue_mask[y][x]),
                                        255,
                                        int(max(0, (((100.0 - self.pcnt) * self.matrix_value[y][x] + self.pcnt * self.matrix_value[y - 1][x]) / 100.0) - fire_value_mask[y][x])))

        for x in range(led.WIDTH):
            led.led_matrix[x][0] = (int(self.hue + fire_hue_mask[0][x]),
                                    255,
                                    int(((100.0 - self.pcnt) * self.matrix_value[0][x] + self.pcnt * self.line[x]) / 100.0))

        self.pcnt = self.pcnt + 12.5


    def adjust(self, delta):
        self.hue = (self.hue + delta) % 256

    def value(self, state):
        self.hue = state

    def getvalue(self):
        return self.hue

# ============================================================================ #

GLYPHS = {
    ":":((0,),
         (0,),
         (0,),
         (1,),
         (0,),
         (1,),
         (0,),
         (0,),
         (0,),
         (0,)),
    "1":((0,0,0),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,0)),
    "2":((0,0,0),
         (1,1,1),
         (0,0,1),
         (0,0,1),
         (1,1,1),
         (1,0,0),
         (1,0,0),
         (1,0,0),
         (1,1,1),
         (0,0,0)),
    "3":((0,0,0),
         (1,1,1),
         (0,0,1),
         (0,0,1),
         (1,1,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (1,1,1),
         (0,0,0)),
    "4":((0,0,0),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,1,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,0)),
    "5":((0,0,0),
         (1,1,1),
         (1,0,0),
         (1,0,0),
         (1,1,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (1,1,1),
         (0,0,0)),
    "6":((0,0,0),
         (1,1,1),
         (1,0,0),
         (1,0,0),
         (1,1,1),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,1,1),
         (0,0,0)),
    "7":((0,0,0),
         (1,1,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,0)),
    "8":((0,0,0),
         (1,1,1),
         (1,0,1),
         (1,0,1),
         (1,1,1),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,1,1),
         (0,0,0)),
    "9":((0,0,0),
         (1,1,1),
         (1,0,1),
         (1,0,1),
         (1,1,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (1,1,1),
         (0,0,0)),
    "0":((0,0,0),
         (1,1,1),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,1,1),
         (0,0,0))
}


class Clock:

    def __init__(self, hue):
        self.position = 0
        self.hue = hue


    @micropython.native
    def update(self):
        self.position = (self.position + 1) % 26

        clockmatrix = [ [0] * led.HEIGHT for _ in range(26) ]

        current_datetime = localtime()
        hours = '%02d' % current_datetime[3]
        minutes = '%02d' % current_datetime[4]

        @micropython.native
        def putglyph(glyph, offset):
            glyphmatrix = GLYPHS[glyph]
            for y in range(len(glyphmatrix)):
                for x in range(len(glyphmatrix[0])):
                    clockmatrix[x + offset][y] = (glyphmatrix[len(glyphmatrix) - 1 - y][x])

        putglyph(hours[0], 0)
        putglyph(hours[1], 4)
        putglyph(':', 8)
        putglyph(minutes[0], 10)
        putglyph(minutes[1], 14)

        sleep_ms(60)

        for x in range(led.WIDTH):
            for y in range(led.HEIGHT):
                if clockmatrix[(x + self.position) % 26][y] == 1:
                    led.led_matrix[x][y] = (self.hue, 170, 255)
                else:
                    led.led_matrix[x][y] = (self.hue, 170, 0)


    def adjust(self, delta):
        self.hue = (self.hue + delta) % 256

    def value(self, state):
        self.hue = state

    def getvalue(self):
        return self.hue
