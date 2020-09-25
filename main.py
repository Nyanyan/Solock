import tkinter
from math import sin, cos, pi

from solver import solver
from detector import detector
#from controller import controller

def create_clock(state=None):
    grid = 28
    offset = 50
    dis = 10
    radius = 20
    canvas.delete()
    for i in range(3):
        for j in range(6):
            x = j * grid + offset + j // 3 * dis
            y = i * grid + offset
            canvas.create_oval(x, y, x + radius, y + radius)
    if state != None:
        clock_place = [[0, 11], [1], [2, 9], [3], [4], [5], [6, 17], [7], [8, 15], [10], [12], [13], [14], [16]]
        clock_mirror = [[False, True], [False], [False, True], [False], [False], [False], [False, True], [False], [False, True], [True], [True], [True], [True], [True]]
        for clock in range(14):
            for tim in range(12):
                deg = 30 * tim
                for i, place in enumerate(clock_place[clock]):
                    x = place % 3 * grid + place // 9 * (grid * 3 + dis) + offset + radius // 2
                    y = place % 9 // 3 * grid + offset + radius // 2
                    r = radius // 5 * 3
                    rad = -1 * -1 ** clock_mirror[clock][i] * deg * pi / 180
                    x_circle = int(x + r * sin(rad))
                    y_circle = int(y - r * cos(rad))
                    canvas.create_oval(x_circle - 1, y_circle - 1, x_circle + 1, y_circle + 1)
            tim = state[clock]
            deg = 30 * tim
            for i, place in enumerate(clock_place[clock]):
                x = place % 3 * grid + place // 9 * (grid * 3 + dis) + offset + radius // 2
                y = place % 9 // 3 * grid + offset + radius // 2
                r = radius // 2
                rad = -1 * -1 ** clock_mirror[clock][i] * deg * pi / 180
                x_circle = int(x + r * sin(rad))
                y_circle = int(y - r * cos(rad))
                canvas.create_line(x_circle, y_circle, x, y)
    canvas.pack()


root = tkinter.Tk()
root.title("Solock")
root.geometry("320x240")
canvas = tkinter.Canvas(root, width = 320, height = 240)

create_clock([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1])

root.mainloop()