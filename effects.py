import led
import uos
import glyph
import encoder
import button
import urandom
import func
import math

# ============================================================================ #

class AllRandom:
    def update(self):
        for x in range(led.WIDTH):
            for y in range(led.HEIGHT):
                led.led_matrix[x][y] = (ord(uos.urandom(1)), ord(uos.urandom(1)), ord(uos.urandom(1)))

# ============================================================================ #

class LoopNumbers:
    def __init__(self, skip):
        self.skip = skip
        self.counter = 0
        self.number = 0

    def update(self):

        if self.counter == 0:
            glyph.put(str(self.number), 0)
            if self.number == 9:
                self.number = 0
            else:
                self.number += 1

        if self.counter == self.skip:
            self.counter = 0
        else:
            self.counter += 1

# ============================================================================ #

class AllHueLoop:

    def __init__(self):
        self.hue = 0

    def update(self):

        led.fill_solid(self.hue, 255, 192)

        if self.hue == 256:
            self.hue = 0
        else:
            self.hue += 1

# ============================================================================ #

class AllHueRotate:
    def update(self):
        led.fill_solid(encoder.value() % 255, 255, 192)

# ============================================================================ #

class AllHueSaturationRotate:

    def __init__(self):
        self.hue = 0
        self.sat = 255
        self.encoder_mode = True
        self.encoder_previous = 0
        self.button_previous = False

    def update(self):

        encoder_current = encoder.value()
        button_current = button.pressed()

        encoder_delta = encoder_current - self.encoder_previous
        self.encoder_previous = encoder_current

        if self.button_previous and not(button_current):
            self.encoder_mode = not(self.encoder_mode)
        self.button_previous = button_current

        if self.encoder_mode:
            self.hue = (self.hue + encoder_delta) % 255
        else:
            self.sat = max(min(self.sat + encoder_delta * 4, 255), 0)

        print("hue=", self.hue, "; sat=", self.sat)

        led.fill_solid(self.hue, self.sat, 127)

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

# ============================================================================ #

class Dawn:

    def __init__(self, dawn_brightness):
        self.dawn_brightness = dawn_brightness
        self.dawn_position = 0

    def update(self):

        dawn_color = (func.remap(self.dawn_position, 0, 255, 10, 35),
                      func.remap(self.dawn_position, 0, 255, 255, 170),
                      func.remap(self.dawn_position, 0, 255, 10, self.dawn_brightness));

        led.fill_solid(*dawn_color)

        if self.dawn_position == 256:
            self.dawn_position = 0
        else:
            self.dawn_position += 1

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

# ============================================================================ #

class Snow:

    def __init__(self, scale):
        self.scale = scale

    def update(self):

        for x in range(led.WIDTH):
            for y in range(led.HEIGHT - 1):
                led.led_matrix[x][y] = led.led_matrix[x][y + 1]

        for x in range(led.WIDTH):
            if led.led_matrix[x][led.HEIGHT - 2][2] == 0 and (urandom.randrange(self.scale) == 0):
                led.led_matrix[x][led.HEIGHT - 1] = [(94, 16, 255), (93, 25, 255), (95, 31, 253), (123, 43, 255)][urandom.randrange(4)]
            else:
                led.led_matrix[x][led.HEIGHT - 1] = (0, 0, 0)

# ============================================================================ #

class Lighters:

    def __init__(self, number, freq):

        self.loading_flag = True

        self.number = number
        self.freq = freq

        self.lighters_pos = [ [0] * self.number for _ in range(2) ]
        self.lighters_speed = [ [0] * self.number for _ in range(2) ]
        self.lighters_color = [(0, 0, 0)] * self.number
        self.loop_counter = 0


    def update(self):

        if self.loading_flag:
            self.loading_flag = False
            for i in range(self.number):
                self.lighters_pos[0][i] = urandom.randrange(led.WIDTH * 10)
                self.lighters_pos[1][i] = urandom.randrange(led.HEIGHT * 10)
                self.lighters_speed[0][i] = urandom.randrange(-10, 10)
                self.lighters_speed[1][i] = urandom.randrange(-10, 10)
                self.lighters_color[i] = (ord(uos.urandom(1)), 255, 255)

        led.fill_solid(0, 0, 0)

        self.loop_counter = (self.loop_counter + 1) % self.freq

        for i in range(self.number):

            if self.loop_counter == 0:
                self.lighters_speed[0][i] = self.lighters_speed[0][i] + urandom.randrange(-3, 4)
                self.lighters_speed[1][i] = self.lighters_speed[1][i] + urandom.randrange(-3, 4)
                self.lighters_speed[0][i] = func.constrain(self.lighters_speed[0][i], -20, 20)
                self.lighters_speed[1][i] = func.constrain(self.lighters_speed[1][i], -20, 20)

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
            self.line[x] = urandom.randrange(64, 255)


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

# ============================================================================ #

class Plasma:

    def __init__(self, speed):
        self.speed = speed
        self.counter = 0

    def update(self):

        self.counter = self.counter + self.speed

        for x in range(led.WIDTH):
            for y in range(led.HEIGHT):
                hue = math.sin( self.counter + x ) + math.sin( self.counter + y / 4.5 ) + math.sin( x + y + self.counter ) + math.sin( math.sqrt( ( x + self.counter ) ** 2.0 + ( y + 1.5 * self.counter ) ** 2.0 ) / 4.0 )
                hue = func.remap(hue, -4, 4, 0, 255)
                led.led_matrix[x][y] = (hue, 255, 255)
