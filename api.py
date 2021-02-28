import utime
import ujson

import led
import effects
import wifi
import alarm


def datetime_string(*dttuple):
    if len(dttuple) == 0:
        utc = utime.localtime()
    else:
        utc = dttuple[0]
    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][utc[6]]
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][utc[1] - 1]
    return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, utc[2], month, utc[0], utc[3], utc[4], utc[5])


def router(payload):
    header = b'HTTP/1.0 200 OK\r\n' + datetime_string() + b'\r\nContent-Type: application/json\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: POST\r\nAccess-Control-Allow-Headers: Content-Type\r\n\r\n'
    try:
        json = ujson.loads(payload)
        action = json['action']
        if action == 'ping':
            return header + ujson.dumps({"error": "OK"})
        elif action == 'geteffects':
            return header + ujson.dumps(geteffects())
        elif action == 'setbrightness':
            value = json['value']
            return header + ujson.dumps(setbrightness(value))
        elif action == 'seteffect':
            index = json['index']
            value = json['value']
            return header + ujson.dumps(seteffect(index, value))
        elif action == 'getsettings':
            return header + ujson.dumps(getsettings())
        elif action == 'savesettings':
            ssid = json['ssid']
            password = json['password']
            timezone = json['timezone']
            maxbrightness = json['maxbrightness']
            return header + ujson.dumps(savesettings(ssid, password, timezone, maxbrightness))
        elif action == 'getalarm':
            return header + ujson.dumps(getalarm())
        elif action == 'savealarm':
            enabled = json['enabled']
            repeat = json['repeat']
            time = json['time']
            before = json['before']
            after = json['after']
            return header + ujson.dumps(savealarm(enabled, repeat, time, before, after))
        else:
            return header + ujson.dumps({"error": "UNKNOWN_METHOD"})
    except KeyError:
        return header + ujson.dumps({"error": "BAD_REQUEST"})
    except ValueError:
        return header


def geteffects():
    if effects.current_effect.__class__.__name__ == 'Dawn':
        effects.current_effect_idx = 3
        effects.next_effect(False)
    return {
        "error": "OK",
        "brightness": led.led_brightness,
        "maxbrightness": led.MAX_BRIGHTNESS,
        "index": effects.current_effect_idx,
        "value": effects.current_effect.getvalue()
    }


def setbrightness(value):
    led.set_brightness(value)
    return {
        "error": "OK"
    }


def seteffect(index, value):
    if effects.current_effect_idx != index:
        effects.current_effect_idx = index
        effects.next_effect(False)
    else:
        effects.current_effect.value(value)
    return {
        "error": "OK"
    }


def getsettings():
    try:
        params_config_file = open('cfg/params.cfg', 'r')
        params_config = [x.strip() for x in params_config_file.readlines()]
        params_config_file.close()
    except:
        return {
            "error": "PARAMS_ERROR"
        }

    try:
        wifi_config_file = open('cfg/wifi.cfg', 'r')
        wifi_config = [x.strip() for x in wifi_config_file.readlines()]
        wifi_config_file.close()
    except OSError:
        wifi_config = ['', '']
    except:
        return {
            "error": "WIFI_ERROR"
        }

    return {
        "error": "OK",
        "ssid": str(wifi_config[0]),
        "password": str(wifi_config[1]),
        "timezone": int(params_config[0]),
        "maxbrightness": int(params_config[1])
    }


def savesettings(ssid, password, timezone, maxbrightness):
    try:
        params_config_file = open('cfg/params.cfg', 'w')
        params_config = [str(timezone), str(maxbrightness)]
        params_config_file.write('\n'.join(params_config))
        params_config_file.close()
    except:
        return {
            "error": "PARAMS_ERROR"
        }

    try:
        wifi_config_file = open('cfg/wifi.cfg', 'w')
        wifi_config = [str(ssid), str(password)]
        wifi_config_file.write('\n'.join(wifi_config))
        wifi_config_file.close()
    except:
        return {
            "error": "WIFI_ERROR"
        }

    return {
        "error": "OK"
    }


def getalarm():
    try:
        alarm_config_file = open('cfg/alarm.cfg', 'r')
        alarm_config = [x.strip() for x in alarm_config_file.readlines()]
        alarm_config_file.close()
    except:
        return {
            "error": "ALARM_ERROR"
        }

    return {
        "error": "OK",
        "apmode": int(wifi.apmode),
        "enabled": int(alarm_config[0]),
        "repeat": int(alarm_config[1]),
        "time": str(alarm_config[2]),
        "before": int(alarm_config[3]),
        "after": int(alarm_config[4])
    }


def savealarm(enabled, repeat, time, before, after):
    try:
        alarm_config_file = open('cfg/alarm.cfg', 'w')
        alarm_config = [str(enabled), str(repeat), str(time)[0:5] + ':00', str(before), str(after)]
        alarm_config_file.write('\n'.join(alarm_config))
        alarm_config_file.close()
    except:
        return {
            "error": "ALARM_ERROR"
        }

    alarm.dawn_alarm.reconfigure(True)

    return {
        "error": "OK"
    }
