import encoderLib


ENCODER_PIN_CLK = 32
ENCODER_PIN_DT = 33

encoder = encoderLib.encoder(ENCODER_PIN_CLK, ENCODER_PIN_DT)

def value():
    return encoder.getValue()
