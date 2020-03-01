import machine


ENCODER_PIN_BUTTON = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)

def pressed():
    return not(bool(ENCODER_PIN_BUTTON.value()))
