import led
import uos
import glyph


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

        for x in range(led.LED_WIDTH):
            for y in range(led.LED_HEIGHT):
                led.led_matrix[x][y] = (self.hue, 255, 192)

        if self.hue == 256:
            self.hue = 0
        else:
            self.hue += 1
