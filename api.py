import utime
import ujson


def datetime_string(*dttuple):
    if len(dttuple) == 0:
        utc = utime.localtime()
    else:
        utc = dttuple[0]
    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][utc[6]]
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][utc[1] - 1]
    return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, utc[2], month, utc[0], utc[3], utc[4], utc[5])

def router(request):
    header = b'HTTP/1.0 200 OK\r\n' + datetime() + b'\r\nContent-Type: application/json\r\n\r\n'
    try:
        json_request = ujson.loads(request)
        action = json_request['action']
        if action == 'savewifisettings':
            return header + ujson.dumps(savewifisettings(json_request['ssid'], json_request['password']))
        else:
            return b'HTTP/1.0 400 Bad Request\r\n' + datetime() + b'\r\n\r\n'
    except KeyError:
        return b'HTTP/1.0 400 Bad Request\r\n' + datetime() + b'\r\n\r\n'
    except ValueError:
        return b'HTTP/1.0 404 Not Found\r\n' + datetime() + b'\r\n\r\n'


def savewifisettings(ssid, password):
    json_response = {
        "error": "ok",
        "ssid": ssid,
        "password": password
    }
    return json_response
