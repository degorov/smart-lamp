import utime
import uos
import usocket
import uselect

import button
import encoder
import led
import wifi
import ntp
import alarm
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


try:
    timezone_config_file = open('cfg/timezone.cfg', 'r')
    timezone = int(timezone_config_file.readline().strip())
    timezone_config_file.close()
    print('Got timezone configuration: ' + str(timezone))
except:
    print('No timezone config file found, setting timezone to +3')
    timezone = 3

dawn_alarm = alarm.Alarm()

if ntp.settime(timezone):
    print('Datetime set from NTP:', api.datetime_string())
    dawn_alarm.reconfigure(True)
else:
    print('Could not sync time from NTP, alarms disabled as well')


http_socket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
http_socket.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
http_socket.bind(('0.0.0.0', 80))
http_socket.listen(1)
http_socket.setblocking(False)

http_poll = uselect.poll()
http_poll.register(http_socket, uselect.POLLIN)


button_previous = button.pressed()
encoder_previous = encoder.value()
encoder_used = False

effects.next_effect(False)


try:
    http_connections = {}; http_requests = {}; http_responses = {}
    while True:

        frame_start_us = utime.ticks_us()

        button_current = button.pressed()
        encoder_current = encoder.value()

        encoder_delta = encoder_current - encoder_previous

        if not button_previous and button_current:
            encoder_used = False

        if not button_current and button_previous and not encoder_used:
            if effects.dawn_mode:
                effects.next_effect(False)
            else:
                effects.next_effect(True)

        if encoder_delta != 0:
            if not button_current:
                if not effects.dawn_mode:
                    led.adjust_brightness(encoder_delta)
            else:
                encoder_used = True
                if not effects.dawn_mode:
                    effects.current_effect.adjust(encoder_delta)

        button_previous = button_current
        encoder_previous = encoder_current


        if dawn_alarm.check():
            effects.dawn_mode = True
            effects.current_effect = effects.Dawn(dawn_alarm.before, dawn_alarm.alarm, dawn_alarm.after, 255)
            dawn_alarm.reconfigure(False)


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
                if http_requests[fileno].startswith(b'OPTIONS / HTTP/') or not http_requests[fileno].endswith(b'\r\n\r\n'):
                    payload = http_requests[fileno].split(b'\r\n')[-1]
                    http_responses[fileno] = api.router(payload)
                    http_poll.modify(socket, uselect.POLLOUT)
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


        effects.current_effect.update()
        if effects.dawn_mode:
            led.render(False)
        else:
            led.render(True)


        frame_end_us = utime.ticks_us()
        # print("fps:", str(int(1000000 / utime.ticks_diff(frame_end_us, frame_start_us))))

finally:
    http_poll.unregister(http_socket)
    http_socket.close()
