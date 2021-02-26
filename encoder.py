from machine import Pin, Timer

ENCODER_PIN_CLK = 32
ENCODER_PIN_DT = 33

clk = Pin(ENCODER_PIN_CLK, Pin.IN, Pin.PULL_UP)
dt = Pin(ENCODER_PIN_DT, Pin.IN, Pin.PULL_UP)

value = 0
encoder_clk_prev = 0

def update(p):
    global encoder_clk_prev, value

    encoder_clk = clk.value()
    encoder_dt = dt.value()

    if not encoder_clk and encoder_clk_prev:
        if encoder_dt:
            value += 1
        else:
            value -= 1
    encoder_clk_prev = encoder_clk

timer = Timer(-1)
timer.init(
    period=1,
    mode=Timer.PERIODIC,
    callback=update
)
