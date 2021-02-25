import led


GLYPHS = {
    ":":((0),
         (0),
         (0),
         (1),
         (0),
         (1),
         (0),
         (0),
         (0),
         (0)),
    "1":((0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1)),
    "2":((1,1,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (1,1,1),
         (1,0,0),
         (1,0,0),
         (1,0,0),
         (1,0,0),
         (1,1,1)),
    "3":((1,1,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (1,1,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (1,1,1)),
    "4":((1,0,1),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,1,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1)),
    "5":((1,1,1),
         (1,0,0),
         (1,0,0),
         (1,0,0),
         (1,1,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (1,1,1)),
    "6":((1,1,1),
         (1,0,0),
         (1,0,0),
         (1,0,0),
         (1,1,1),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,1,1)),
    "7":((1,1,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1)),
    "8":((1,1,1),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,1,1),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,1,1)),
    "9":((1,1,1),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,1,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (0,0,1),
         (1,1,1)),
    "0":((1,1,1),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,0,1),
         (1,1,1))
}


def put(glyph_key, column):
    glyph_matrix = GLYPHS[glyph_key]
    for y in range(len(glyph_matrix)):
        for x in range(len(glyph_matrix[0])):
            led.led_matrix[x + column][y] = (0, 0, glyph_matrix[len(glyph_matrix) - 1 - y][x] * 255)