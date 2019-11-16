import led
import uos


def all_random():
    for x in range(led.LED_WIDTH):
        for y in range(led.LED_HEIGHT):
            led.led_matrix[x][y] = (ord(uos.urandom(1)), ord(uos.urandom(1)), int(ord(uos.urandom(1)) / 2))
