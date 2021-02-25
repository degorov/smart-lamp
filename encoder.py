from machine import Pin
from machine import Timer

ENCODER_PIN_CLK = 32
ENCODER_PIN_DT = 33

class Encoder:
    encoder_clk_prev = False
    i = 0

    def __init__(self, clk_pin, dt_pin):
        self.clk = Pin(clk_pin, Pin.IN, Pin.PULL_UP)
        self.dt = Pin(dt_pin, Pin.IN, Pin.PULL_UP)

        tim = Timer(-1)
        tim.init(
            period=1,
            mode=Timer.PERIODIC,
            callback=self.update
        )

    def getValue(self):
        return(self.i)

    def update(self, p):
        self.encoder_clk = self.clk.value()
        self.encoder_dt = self.dt.value()

        if not self.encoder_clk and self.encoder_clk_prev:
            if self.encoder_dt:
                self.i += 1
            else:
                self.i -= 1

        self.encoder_clk_prev = self.encoder_clk


encoder = Encoder(ENCODER_PIN_CLK, ENCODER_PIN_DT)

def value():
    return encoder.getValue()
