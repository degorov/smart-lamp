import machine
import esp
import utime
import uos
import usocket
import uselect

import encoder
import wifi
import ntp
import http


LED_PIN = machine.Pin(4, machine.Pin.OUT)
ENCODER_PIN_A = machine.Pin(32, machine.Pin.IN, machine.Pin.PULL_UP)
ENCODER_PIN_B = machine.Pin(33, machine.Pin.IN, machine.Pin.PULL_UP)
ENCODER_PIN_BUTTON = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)

LED_WIDTH = 8
LED_HEIGHT = 10

GLYPH_DATA = {
    ":": ((0,0,0,1,0,1,0,0,0,0),),
    "1": ((0,0,0,0,0,0,0,0,0,0),
          (0,0,0,0,0,0,0,0,0,0),
          (1,1,1,1,1,1,1,1,1,1)),
    "2": ((1,0,0,0,1,1,1,1,1,1),
          (1,0,0,0,1,0,0,0,0,1),
          (1,1,1,1,1,0,0,0,0,1)),
    "3": ((1,0,0,0,1,0,0,0,0,1),
          (1,0,0,0,1,0,0,0,0,1),
          (1,1,1,1,1,1,1,1,1,1)),
    "4": ((1,1,1,1,1,0,0,0,0,0),
          (0,0,0,0,1,0,0,0,0,0),
          (1,1,1,1,1,1,1,1,1,1)),
    "5": ((1,1,1,1,1,0,0,0,0,1),
          (1,0,0,0,1,0,0,0,0,1),
          (1,0,0,0,1,1,1,1,1,1)),
    "6": ((1,1,1,1,1,1,1,1,1,1),
          (1,0,0,0,1,0,0,0,0,1),
          (1,0,0,0,1,1,1,1,1,1)),
    "7": ((1,0,0,0,0,0,0,0,0,0),
          (1,0,0,0,0,0,0,0,0,0),
          (1,1,1,1,1,1,1,1,1,1)),
    "8": ((1,1,1,1,1,1,1,1,1,1),
          (1,0,0,0,1,0,0,0,0,1),
          (1,1,1,1,1,1,1,1,1,1)),
    "9": ((1,1,1,1,1,0,0,0,0,1),
          (1,0,0,0,1,0,0,0,0,1),
          (1,1,1,1,1,1,1,1,1,1)),
    "0": ((1,1,1,1,1,1,1,1,1,1),
          (1,0,0,0,0,0,0,0,0,1),
          (1,1,1,1,1,1,1,1,1,1))
}


led_map = [[((LED_HEIGHT * (LED_WIDTH - 1)) - LED_HEIGHT * x + y) * 3 if not(x % 2) else ((LED_HEIGHT * (LED_WIDTH - 1) - 1) - LED_HEIGHT * (x - 1) - y) * 3 for y in range(LED_HEIGHT)] for x in range(LED_WIDTH)]

led_matrix = [ [(0, 0, 0)] * LED_HEIGHT for _ in range(LED_WIDTH) ]

led_buffer = bytearray(LED_HEIGHT * LED_WIDTH * 3)

enc = encoder.Encoder(ENCODER_PIN_A, ENCODER_PIN_B, 0, 1)


def scale8(i, scale):
    return (i * (1 + scale)) >> 8

def scale8_video(i, scale):
    return ((i * scale) >> 8) + (1 if (i and scale) else 0)

# inputs are all in range 0-255

def hsv_to_rainbow_rgb(hue, sat, val):

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



def put_glyph(glyph_key, column):
    glyph = GLYPH_DATA[glyph_key]
    for x in range(len(glyph)):
        for y in range(LED_HEIGHT):
            led_matrix[x + column][y] = (0, 0, glyph[x][y] * 255)


def render_led_matrix():
    for x in range(LED_WIDTH):
        for y in range(LED_HEIGHT):
            idx = led_map[x][y]
            led_buffer[idx], led_buffer[idx + 1], led_buffer[idx + 2] = hsv_to_rainbow_rgb(*led_matrix[x][y])
    esp.neopixel_write(LED_PIN, led_buffer, 1)



if ENCODER_PIN_BUTTON.value():
    try:
        wifi_config_file = open('wifi.cfg', 'r')
        wifi_config = [x.strip() for x in wifi_config_file.readlines()]
        wifi_config_file.close()
        print('Got network configuration:' + str(wifi_config))
        if wifi.connect(wifi_config):
            pass
        else:
            pass
    except OSError:
        print('No Wi-Fi config file found')
        wifi.hotspot()
else:
    try:
        uos.remove('wifi.cfg')
    finally:
        print('Wi-Fi configuration reset')
        wifi.hotspot()


ntp.settime()
print('Datetime set:', http.header_date())


WS_EOL1 = b'\n\n'
WS_EOL2 = b'\n\r\n'

http_socket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
http_socket.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
http_socket.bind(('0.0.0.0', 80))
http_socket.listen(1)
http_socket.setblocking(False)

http_poll = uselect.poll()
http_poll.register(http_socket, uselect.POLLIN)


try:
    http_connections = {}; http_requests = {}; http_responses = {}
    while True:

        frame_start_us = utime.ticks_us()

        events = http_poll.poll(0)
        for socket, event in events:
            fileno = socket.fileno()
            if socket == http_socket:
                connection, address = http_socket.accept()
                connection.setblocking(False)
                http_poll.register(connection, uselect.POLLIN)
                fileno = connection.fileno()
                http_connections[fileno] = connection
                http_requests[fileno] = b''
                http_responses[fileno] = b''
            elif event & uselect.POLLIN:
                http_requests[fileno] += http_connections[fileno].recv(1024)
                if WS_EOL1 in http_requests[fileno] or WS_EOL2 in http_requests[fileno]:
                    http_poll.modify(socket, uselect.POLLOUT)
                    request = http_requests[fileno].decode().split('\n')[-1]
                    http_responses[fileno] = http.router(request)
            elif event & uselect.POLLOUT:
                byteswritten = http_connections[fileno].send(http_responses[fileno])
                http_responses[fileno] = http_responses[fileno][byteswritten:]
                if len(http_responses[fileno]) == 0:
                    http_poll.modify(socket, 0)
                    http_connections[fileno].close()
            elif event & uselect.POLLHUP:
                http_poll.unregister(socket)
                http_connections[fileno].close()
                del http_connections[fileno]

        for x in range(LED_WIDTH):
            for y in range(LED_HEIGHT):
                led_matrix[x][y] = (ord(uos.urandom(1)), ord(uos.urandom(1)), int(ord(uos.urandom(1)) / 2))
        render_led_matrix()

        frame_end_us = utime.ticks_us()
        print("fps:", str(int(1000000 / (frame_end_us - frame_start_us))))

finally:
    http_poll.unregister(http_socket)
    http_socket.close()

