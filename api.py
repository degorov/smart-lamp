import utime
import ujson

import led


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
        else:
            return header + ujson.dumps({"error": "UNKNOWN_METHOD"})
    except KeyError:
        return header + ujson.dumps({"error": "BAD_REQUEST"})
    except ValueError:
        return header

def geteffects():
    return {
        "error": "OK",
        "brightness": led.led_brightness,
        "maxbrightness": led.MAX_BRIGHTNESS
    }

def setbrightness(value):
    led.set_brightness(value)
    return {
        "error": "OK"
    }
