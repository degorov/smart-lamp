try:
    import uos
    import urandom
except:
    import os as uos
    import random as urandom

import led
import math


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
        if current_effect_idx == 9:
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
        current_effect = VerticalRainbow(4)
    elif current_effect_idx == 4:
        current_effect = HorizontalRainbow(4)
    elif current_effect_idx == 5:
        current_effect = Matrix(40, 20)
    elif current_effect_idx == 6:
        current_effect = Sparkles(4, 16)
    elif current_effect_idx == 7:
        current_effect = Lighters(5, 8)
    elif current_effect_idx == 8:
        current_effect = Plasma(0.1)
    elif current_effect_idx == 9:
        current_effect = Fire(0, 1)

# ============================================================================ #

class Void:

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

    def update(self):
        self.position = (self.position + self.speed) % 256
        for x in range(led.WIDTH):
            for y in range(led.HEIGHT):
                led.led_matrix[x][y] = (int(y * 256 / led.HEIGHT) - self.position, 255, 255)

    def adjust(self, delta):
        self.speed = constrain(self.speed + delta, -16, 16)

    def value(self, state):
        self.speed = state - 16

    def getvalue(self):
        return self.speed + 16

# ============================================================================ #

class HorizontalRainbow:

    def __init__(self, speed):
        self.position = 0
        self.speed = speed

    def update(self):
        self.position = (self.position + self.speed) % 256
        for x in range(led.WIDTH):
            for y in range(led.HEIGHT):
                led.led_matrix[x][y] = (int(x * 256 / led.WIDTH) - self.position, 255, 255)

    def adjust(self, delta):
        self.speed = constrain(self.speed + delta, -16, 16)

    def value(self, state):
        self.speed = state - 16

    def getvalue(self):
        return self.speed + 16

# ============================================================================ #

class Matrix:

    def __init__(self, scale, step):
        self.scale = scale
        self.step = step

    def update(self):

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

class Fire:

    def __init__(self, hue_rotation, sparkles):

        self.loading_flag = True

        self.hue_rotation = hue_rotation
        self.sparkles = sparkles

        self.line = [0] * led.WIDTH
        self.pcnt = 0

        self.matrix_value = [ [0] * 10 for _ in range(8) ]

        self.value_mask = ((32 , 32 , 0  , 0  , 0  , 0 , 0 , 0  , 0  , 0  ),
                           (64 , 64 , 0  , 0  , 0  , 0 , 0 , 0  , 0  , 0  ),
                           (96 , 96 , 32 , 0  , 0  , 0 , 0 , 0  , 0  , 32 ),
                           (128, 128, 64 , 32 , 0  , 0 , 0 , 0  , 32 , 64 ),
                           (160, 160, 96 , 64 , 32 , 0 , 0 , 32 , 64 , 96 ),
                           (192, 192, 128, 96 , 64 , 32, 32, 64 , 96 , 128),
                           (255, 255, 160, 128, 96 , 64, 64, 96 , 128, 160),
                           (255, 255, 192, 160, 128, 96, 96, 128, 160, 192))

        self.hue_mask = ((1 , 1 , 11, 19, 22, 25, 25, 22, 19, 11),
                         (1 , 1 , 8 , 13, 19, 22, 22, 19, 13, 8 ),
                         (1 , 1 , 8 , 13, 16, 19, 19, 16, 13, 8 ),
                         (1 , 1 , 5 , 11, 13, 16, 16, 13, 11, 5 ),
                         (1 , 1 , 5 , 11, 11, 13, 13, 11, 11, 5 ),
                         (0 , 0 , 1 , 5 , 8 , 11, 11, 8 , 5 , 1 ),
                         (0 , 0 , 0 , 1 , 5 , 8 , 8 , 5 , 1 , 0 ),
                         (0 , 0 , 0 , 0 , 1 , 5 , 5 , 1 , 0 , 0 ))


    def generate_line(self):
        for x in range(led.WIDTH):
            self.line[x] = urandom.randrange(64, 256)


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

        for y in range(led.HEIGHT - 1, 0, -1):
            for x in range(0, led.WIDTH):
                if y < 8:
                    led.led_matrix[x][y] = (int(self.hue_rotation + self.hue_mask[y][x]),
                                            255,
                                            int(max(0, (((100.0 - self.pcnt) * self.matrix_value[y][x] + self.pcnt * self.matrix_value[y - 1][x]) / 100.0) - self.value_mask[y][x])))
                elif y == 8 and self.sparkles:
                    if (urandom.randrange(0, 20) == 0) and led.led_matrix[x][y - 1][2] > 0:
                        led.led_matrix[x][y] = led.led_matrix[x][y - 1]
                    else:
                        led.led_matrix[x][y] = (0, 0, 0)
                elif self.sparkles:
                    if led.led_matrix[x][y - 1][2] > 0:
                        led.led_matrix[x][y] = led.led_matrix[x][y - 1]
                    else:
                        led.led_matrix[x][y] = (0, 0, 0)

        for x in range(led.WIDTH):
            led.led_matrix[x][0] = (int(self.hue_rotation + self.hue_mask[0][x]),
                                    255,
                                    int(((100.0 - self.pcnt) * self.matrix_value[0][x] + self.pcnt * self.line[x]) / 100.0))

        self.pcnt = self.pcnt + 30


    def adjust(self, delta):
        if delta < 0:
            self.sparkles = 0
        if delta > 0:
            self.sparkles = 1

    def value(self, state):
        self.sparkles = state

    def getvalue(self):
        return self.sparkles
