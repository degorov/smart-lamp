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

led.loading_rings(10)

try: uos.mkdir('cfg')
except OSError: pass
finally: led.loading_rings(20)

if button.pressed():
    try: uos.remove('cfg/params.cfg')
    except: pass
    try: uos.remove('cfg/alarm.cfg')
    except: pass
    try: uos.remove('cfg/wifi.cfg')
    except: pass
    finally:
        print('Wi-Fi configuration reset')
        wifi.hotspot()
else:
    try:
        wifi_config_file = open('cfg/wifi.cfg', 'r')
        wifi_config = [x.strip() for x in wifi_config_file.readlines()]
        wifi_config_file.close()
        print('Got network configuration:' + str(wifi_config))
        led.loading_rings(30)
        if wifi.connect(wifi_config):
            led.loading_rings(40)
        else:
            raise Exception('Wi-Fi not connected')
    except OSError:
        print('No Wi-Fi config file found')
        wifi.hotspot()

try:
    params_config_file = open('cfg/params.cfg', 'r')
    params_config = [x.strip() for x in params_config_file.readlines()]
    timezone = int(params_config[0])
    led.MAX_BRIGHTNESS = int(params_config[1])
    led.led_brightness = led.MAX_BRIGHTNESS
    params_config_file.close()
    print('Got timezone configuration: ' + str(timezone))
    print('Got brightness configuration: ' + str(led.MAX_BRIGHTNESS))
except:
    params_config_file = open('cfg/params.cfg', 'w')
    timezone = 3
    params_config = [str(timezone), str(led.MAX_BRIGHTNESS)]
    params_config_file.write('\n'.join(params_config))
    params_config_file.close()
    print('No timezone specified, setting timezone to +3')
    print('No brightness specified, assuming %d' % (led.MAX_BRIGHTNESS))
finally:
    led.loading_rings(50)

dawn_alarm = alarm.dawn_alarm
led.loading_rings(60)

if ntp.settime(timezone):
    print('Datetime set from NTP:', api.datetime_string())
else:
    if not wifi.apmode:
        raise Exception('NTP not synced')

led.loading_rings(70)
dawn_alarm.reconfigure(True)
led.loading_rings(80)


def httpserver():

    global connections, requests, responses, server, poll
    connections = {}; requests = {}; responses = {}

    server = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    server.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 80))
    server.listen(1)
    server.setblocking(False)

    poll = uselect.poll()
    poll.register(server, uselect.POLLIN)

    print('Started HTTP server')


httpserver()
led.loading_rings(90)

button_previous = button.pressed()
encoder_previous = encoder.value
encoder_used = False

led.loading_rings(100)
effects.next_effect(False)

# frame_time_p = utime.ticks_us()

while True:

    button_current = button.pressed()
    encoder_current = encoder.value

    encoder_delta = encoder_current - encoder_previous

    if not button_previous and button_current:
        encoder_used = False

    if not button_current and button_previous and not encoder_used:
        if effects.current_effect.__class__.__name__ == 'Dawn':
            effects.next_effect(False)
        else:
            effects.next_effect(True)

    if encoder_delta != 0:
        if not button_current:
            if not effects.current_effect.__class__.__name__ == 'Dawn':
                led.adjust_brightness(encoder_delta)
        else:
            encoder_used = True
            if not effects.current_effect.__class__.__name__ == 'Dawn':
                effects.current_effect.adjust(encoder_delta)

    button_previous = button_current
    encoder_previous = encoder_current

    if dawn_alarm.check():
        effects.current_effect = alarm.Dawn(dawn_alarm.before, dawn_alarm.alarm, dawn_alarm.after)
        dawn_alarm.reconfigure(False)

    effects.current_effect.update()
    if effects.current_effect.__class__.__name__ == 'Dawn':
        led.render(False)
    else:
        led.render(True)

    # frame_time = utime.ticks_us()
    # print("fps:", str(int(1000000 / utime.ticks_diff(frame_time, frame_time_p))))
    # frame_time_p = frame_time

    try:
        events = poll.poll(0)
        for socket, event in events:
            fileno = socket.fileno()
            if socket == server:
                connection, address = server.accept()
                connection.setblocking(False)
                poll.register(connection, uselect.POLLIN)
                fileno = connection.fileno()
                connections[fileno] = connection
                requests[fileno] = b''
                responses[fileno] = b''
            elif event & uselect.POLLIN:
                requests[fileno] += connections[fileno].recv(768)
                if not requests[fileno].startswith(b'POST / HTTP/') or not requests[fileno].endswith(b'\r\n\r\n'):
                    payload = requests[fileno].split(b'\r\n')[-1]
                    responses[fileno] = api.router(payload)
                    poll.modify(socket, uselect.POLLOUT)
            elif event & uselect.POLLOUT:
                byteswritten = connections[fileno].send(responses[fileno])
                responses[fileno] = responses[fileno][byteswritten:]
                if len(responses[fileno]) == 0:
                    poll.modify(socket, 0)
                    connections[fileno].close()
                    del connections[fileno]
                    del requests[fileno]
                    del responses[fileno]
            elif event & uselect.POLLHUP:
                poll.unregister(socket)
                connections[fileno].close()
                del connections[fileno]
                del requests[fileno]
                del responses[fileno]
    except Exception as e:
        print(e)
        poll.unregister(server)
        server.close()
        httpserver()
