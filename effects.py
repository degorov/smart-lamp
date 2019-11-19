import led
import uos
import glyph
import encoder
import button
import urandom
import func

# ============================================================================ #

class AllRandom:
    def update(self):
        for x in range(led.LED_WIDTH):
            for y in range(led.LED_HEIGHT):
                led.led_matrix[x][y] = (ord(uos.urandom(1)), ord(uos.urandom(1)), int(ord(uos.urandom(1)) / 2))

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

        for x in range(led.LED_WIDTH):
            this_color_v = led.led_matrix[x][0][2]
            if this_color_v == 0:
                led.led_matrix[x][0] = (96, 255, 255 * (urandom.randrange(self.scale) == 0))
            elif this_color_v < self.step:
                led.led_matrix[x][0] = (0, 0, 0)
            else:
                led.led_matrix[x][0] = (96, 255, this_color_v - self.step)

        for x in range(led.LED_WIDTH):
            for y in range(led.LED_HEIGHT - 1, 0, -1):
                led.led_matrix[x][y] = led.led_matrix[x][y - 1]

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
