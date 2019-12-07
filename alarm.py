import utime
import machine
import api


def reconfigure():

    try:
        alarm_config_file = open('cfg/alarm.cfg', 'r')
        alarm_config = [x.strip() for x in alarm_config_file.readlines()]
        alarm_config_file.close()
        print('Got alarm configuration:', alarm_config)
    except:
        print('No alarm config file found')

    alarm_config_enabled = int(alarm_config[0])

    if alarm_config_enabled:

        alarm_config_repeat = [int(alarm_config[1]) >> i & 1 for i in range(6, -1, -1)]        # 0-6 mon-sun
        alarm_config_time_h, alarm_config_time_m, alarm_config_time_s = map(int, alarm_config[2].split(':'))
        alarm_config_before = int(alarm_config[3])
        alarm_config_after = int(alarm_config[4])

        current_datetime = utime.localtime()
        current_timestamp = utime.time()
        current_day_of_week = current_datetime[6]

        alarm_timestamp = utime.mktime((current_datetime[0], current_datetime[1], current_datetime[2], alarm_config_time_h, alarm_config_time_m, alarm_config_time_s, current_datetime[6], current_datetime[7]))
        alarm_shift = 0

        if 1 not in alarm_config_repeat:
            if alarm_timestamp <= current_timestamp:
                alarm_shift = 86400
        else:
            if alarm_config_repeat[current_day_of_week]:
                if alarm_timestamp <= current_timestamp:
                    while True:
                        current_day_of_week = (current_day_of_week + 1) % 7
                        alarm_shift = alarm_shift + 86400
                        if alarm_config_repeat[current_day_of_week]:
                            break
            else:
                while True:
                    current_day_of_week = (current_day_of_week + 1) % 7
                    alarm_shift = alarm_shift + 86400
                    if alarm_config_repeat[current_day_of_week]:
                        break

        alarm_timestamp = alarm_timestamp + alarm_shift

        print('Alarm set to:', api.datetime_string(utime.localtime(alarm_timestamp)))
        # machine.RTC().alarm(time=)

    else:
        print('Alarm disabled in settings')
        # machine.RTC().alarm(time=)
