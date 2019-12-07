import utime
import uos
import usocket
import uselect

import button
import encoder
import led
import wifi
import ntp
import api
import effects


if button.pressed():
    try:
        uos.remove('cfg/wifi.cfg')
    except:
        pass
    finally:
        print('Wi-Fi configuration reset')
        wifi.hotspot()
else:
    try:
        wifi_config_file = open('cfg/wifi.cfg', 'r')
        wifi_config = [x.strip() for x in wifi_config_file.readlines()]
        wifi_config_file.close()
        print('Got network configuration:' + str(wifi_config))
        if wifi.connect(wifi_config):
            pass
        else:
            pass
    except:
        print('No Wi-Fi config file found')
        wifi.hotspot()


if ntp.settime():
    print('Datetime set from NTP:', api.datetime())
else:
    print('Could not sync time from NTP')


effect = effects.Void()
# effect = effects.AllRandom()
# effect = effects.LoopNumbers(10)
# effect = effects.AllHueLoop()
# effect = effects.AllHueRotate()
# effect = effects.AllHueSaturationRotate()
# effect = effects.Matrix(40, 20)
# effect = effects.Dawn(192)
# effect = effects.Sparkles(8, 16)
# effect = effects.Snow(30)
# effect = effects.Lighters(10, 32)
# effect = effects.Fire(0, 1)
# effect = effects.Plasma(0.1)


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
                if b'\n\n' in http_requests[fileno] or b'\n\r\n' in http_requests[fileno]:
                    http_poll.modify(socket, uselect.POLLOUT)
                    request = http_requests[fileno].decode().split('\n')[-1]
                    http_responses[fileno] = api.router(request)
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

        effect.update()
        led.render()

        # print(encoder.value())
        # utime.sleep_ms(100)

        frame_end_us = utime.ticks_us()
        print("fps:", str(int(1000000 / utime.ticks_diff(frame_end_us, frame_start_us))))

finally:
    http_poll.unregister(http_socket)
    http_socket.close()
