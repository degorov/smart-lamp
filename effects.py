import led
import uos
import glyph


# ============================================================================ #

def all_random():
    for x in range(led.LED_WIDTH):
        for y in range(led.LED_HEIGHT):
            led.led_matrix[x][y] = (ord(uos.urandom(1)), ord(uos.urandom(1)), int(ord(uos.urandom(1)) / 2))

# ============================================================================ #

loop_numbers_counter = 0
loop_numbers_number = 0

def loop_numbers():
    global loop_numbers_counter
    global loop_numbers_number

    if loop_numbers_counter == 0:
        glyph.put(str(loop_numbers_number), 0)
        if loop_numbers_number == 9:
            loop_numbers_number = 0
        else:
            loop_numbers_number += 1

    if loop_numbers_counter == 10:
        loop_numbers_counter = 0
    else:
        loop_numbers_counter += 1

# ============================================================================ #

all_hue_loop_hue = 0

def all_hue_loop():
    global all_hue_loop_hue

    for x in range(led.LED_WIDTH):
        for y in range(led.LED_HEIGHT):
            led.led_matrix[x][y] = (all_hue_loop_hue, 255, 192)

    if all_hue_loop_hue == 256:
        all_hue_loop_hue = 0
    else:
        all_hue_loop_hue += 1
