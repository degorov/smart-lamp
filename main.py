import gc
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

led.fill_solid(0, 0, 0)
led.render(True)

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


server = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
server.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 80))
server.listen(1)
server.setblocking(False)

poll = uselect.poll()
poll.register(server, uselect.POLLIN)

connections = {}; requests = {}; responses = {}

button_previous = button.pressed()
encoder_previous = encoder.value
encoder_used = False

effects.next_effect(False)

frame_time_p = utime.ticks_us()

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
        effects.current_effect = effects.Dawn(dawn_alarm.before, dawn_alarm.alarm, dawn_alarm.after, 255)
        dawn_alarm.reconfigure(False)

    effects.current_effect.update()
    if effects.current_effect.__class__.__name__ == 'Dawn':
        led.render(False)
    else:
        led.render(True)

    frame_time = utime.ticks_us()
    # print("fps:", str(int(1000000 / utime.ticks_diff(frame_time, frame_time_p))))
    frame_time_p = frame_time

    gc.collect()
    # print(gc.mem_free())

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
                requests[fileno] += connections[fileno].recv(512)
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
