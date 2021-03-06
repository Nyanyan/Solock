# coding:utf-8

import tkinter
from math import sin, cos, pi

from solver import solver
from detector import detector
from controller import controller

def create_clock(state=None):
    global canvas, inspection, start_medium, solvingtimevar, solvingtime
    grid = 28
    offset = 50
    dis = 10
    radius = 20
    canvas.delete("all")

    inspection = tkinter.Button(root, text="inspection", command=inspection_p)
    inspection.place(x=0, y=0)

    start_medium = tkinter.Button(root, text="start", command=start_medium_p)
    start_medium.place(x=250, y=0)

    solvingtimevar = tkinter.StringVar(master=root, value='info')
    solvingtime = tkinter.Label(textvariable=solvingtimevar)
    solvingtime.place(x=120, y=20)

    for i in range(3):
        for j in range(6):
            x = j * grid + offset + j // 3 * dis
            y = i * grid + offset
            canvas.create_oval(x, y, x + radius, y + radius)
    if state != None:
        clock_place = [[0, 11], [1], [2, 9], [3], [4], [5], [6, 17], [7], [8, 15], [10], [12], [13], [14], [16]]
        clock_mirror = [[False, True], [False], [False, True], [False], [False], [False], [False, True], [False], [False, True], [False], [False], [False], [False], [False]]
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


def inspection_p():
    global state, solution
    solution = []
    state = [-1 for _ in range(14)]
    def inspection_upper_p():
        global state
        state[:9] = detector(1)
    def inspection_lower_p():
        global state
        state[9:] = detector(0)
    def inspection_finish_p():
        global state, solution
        if -1 in set(state):
            print('NG', state)
            return
        inspection_lower.place_forget()
        inspection_upper.place_forget()
        inspection_finish.place_forget()
        solution, cost = solver(state)
        print(state)
        print(cost)
        #print(solution)
        #with open('log.txt', mode='w') as f:
        #    f.write(str(state) + '\n')
        #    f.write(str(solution) + '\n')
        create_clock(state)
    inspection_upper = tkinter.Button(root, text="upper", command=inspection_upper_p)
    inspection_upper.place(x=0, y=25)
    inspection_lower = tkinter.Button(root, text="lower", command=inspection_lower_p)
    inspection_lower.place(x=0, y=50)
    inspection_finish = tkinter.Button(root, text="finish", command=inspection_finish_p)
    inspection_finish.place(x=0, y=75)

def start_medium_p():
    solvingtimevar.set(controller(solution, 560, 0.079, 1.0)) # 440, 0.085, 1.0


solution = []
state = [-1 for _ in range(14)]
root = tkinter.Tk()
root.title("Solock")
root.geometry("320x240")

canvas = tkinter.Canvas(root, width = 320, height = 240)

inspection = tkinter.Button(root, text="inspection", command=inspection_p)
inspection.place(x=0, y=0)

start_medium = tkinter.Button(root, text="start", command=start_medium_p)
start_medium.place(x=250, y=0)

solvingtimevar = tkinter.StringVar(master=root, value='info')
solvingtime = tkinter.Label(textvariable=solvingtimevar)
solvingtime.place(x=120, y=20)

create_clock()

print('main initialized')

root.mainloop()