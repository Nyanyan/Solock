import tkinter
from math import sin, cos, pi

from solver import solver
from detector import detector
#from controller import controller

root = tkinter.Tk()
root.title("Solock")
root.geometry("320x240")
canvas = tkinter.Canvas(root, width = 320, height = 240)

grid = 20
offset = 50
dis = 10
radius = 20

for i in range(3):
    for j in range(6):
        x = j * grid + offset + j // 3 * dis
        y = i * grid + offset
        canvas.create_oval(x, y, x + radius, y + radius)

clocks = [[None for _ in range(12)] for _ in range(14)]
clock_place = [[0, 11], [1], [2, 9], [3], [4], [5], [6, 17], [7], [8, 15], [10], [12], [13], [14], [16]]
clock_mirror = [[False, True], [False], [False, True], [False], [False], [False], [False, True], [False], [False, True], [True], [True], [True], [True], [True]]
for clock in range(14):
    for tim in range(12):
        clocks[clock][tim] = tkinter.Canvas(root, width = 320, height = 240)
        deg = 30 * tim
        for i, place in enumerate(clock_place[clock]):
            x = place % 3 * grid + place // 9 * (grid * 3 + dis) + offset + radius // 2
            y = place % 9 // 3 * grid + offset + radius // 2
            r = 8
            rad = -1 ** clock_mirror[clock][i] * deg * pi / 180
            x_circle = int(x + r * sin(rad))
            y_circle = int(y - r * cos(rad))
            clocks[clock][tim].create_oval(x_circle - 2, y_circle - 2, x_circle + 2, y_circle + 2)
        clocks[clock][tim].pack()

canvas.pack()
root.mainloop()