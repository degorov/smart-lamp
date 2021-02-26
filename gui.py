from tkinter import *

from led import WIDTH, HEIGHT, led_matrix, hsv_to_rainbow_rgb
import effects

SIZE = 32
FPS = 15

window = Tk()
window.title("Smart Lamp Effects GUI")
window.resizable(0, 0)

canvas = Canvas(window, bg='#000000', width=WIDTH * SIZE, height=HEIGHT * SIZE)
listbox = Listbox(window)

listbox.pack(side="left", fill="both", expand=True)
canvas.pack(side="right")

listbox.insert(0, 'Void')
listbox.insert(1, 'AllHueRotate')
listbox.insert(2, 'AllHueLoop')
listbox.insert(3, 'Matrix')
listbox.insert(4, 'Sparkles')
listbox.insert(5, 'Lighters')
listbox.insert(6, 'Fire')
listbox.insert(7, 'Plasma')

def seleffect(event):
    sel = event.widget.curselection()
    if sel:
        effindex = sel[0]
    effects.current_effect_idx = effindex
    effects.next_effect(False)

listbox.bind("<<ListboxSelect>>", seleffect)

def adjp():
    effects.current_effect.adjust(4)

def adjm():
    effects.current_effect.adjust(-4)

def value():
    try:
        effects.current_effect.value(int(state.get()))
    except:
        pass

buttonP = Button(window, text ="PLUS", command = adjp)
buttonM = Button(window, text ="MINUS", command = adjm)

buttonP.pack()
buttonM.pack()

state = Entry(window)
state.pack()

buttonV = Button(window, text ="APPLY", command = value)
buttonV.pack()

diodes = [['rect_%d_%d' % (i, j) for i in range(HEIGHT)] for j in range(WIDTH)]

for x in range(WIDTH):
    for y in range(HEIGHT):
        canvas.create_rectangle(x * SIZE, (HEIGHT - y - 1) * SIZE, (x * SIZE + SIZE), (HEIGHT - y - 1) * SIZE + SIZE, fill='red', width=0, tag=diodes[x][y])

effects.current_effect_idx = 0
effects.next_effect(False)

def task():
    window.after(round(1 / FPS * 1000), task)

    effects.current_effect.update()

    for x in range(WIDTH):
        for y in range(HEIGHT):
            r, g, b = hsv_to_rainbow_rgb(led_matrix[x][y][0], led_matrix[x][y][1], led_matrix[x][y][2], False)
            canvas.itemconfig(diodes[x][y], fill='#%02x%02x%02x' % (int(r), int(g), int(b)))

task()

window.mainloop()
