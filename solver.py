'''
clock numbering

upper
 0  1  2
 3  4  5
 6  7  8

lower
 2  9  0
10 11 12
 8 13  6

solved: Cube.state == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

pin numbering

upper
0 1
2 3
'''

from itertools import combinations

def y_move_clocks(pins, direction):
    res = []
    if direction: # move upper clocks
        clock_candidate = [[0, 1, 3, 4], [1, 2, 4, 5], [3, 4, 6, 7], [4, 5, 7, 8]]
        for i, j in enumerate(pins):
            if j:
                res.extend(clock_candidate[i])
    else: # move lower clocks
        clock_candidate = [[0, 9, 12, 11], [9, 2, 11, 10], [12, 11, 6, 13], [11, 10, 13, 8]]
        for i, j in enumerate(pins):
            if not j:
                res.extend(clock_candidate[i])
    res = set(res)
    return res

def n_move_clocks(pins, direction):
    res = set(range(14)) - y_move_clocks(pins, direction)
    return res

def move(state, pins, direction, twist):
    move_clocks = y_move_clocks(pins, direction)
    res = [i for i in state]
    for i in move_clocks:
        res[i] += twist
        res[i] %= 12
    return res

scrambled_cube = [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0] # UR1+
solution = []

def search(depth, state, banned_pins):
    global solution
    for direction in range(2): # 0: lower, 1: upper
        pin_candidate = range(1, 5) if direction else range(4)
        for num_of_pins in pin_candidate: # pins that are pulled
            for pins in combinations(range(4), num_of_pins):
                if set(pins) in banned_pins[direction]:
                    continue
                move_clocks_time = [state[i] for i in y_move_clocks(pins, direction)]
                not_move_clocks = n_move_clocks(pins, direction)
                if direction:
                    not_move_clocks -= set([9, 10, 11, 12, 13])
                else:
                    not_move_clocks -= set([1, 3, 4, 5, 7])
                time_candidate = [state[i] for i in not_move_clocks]
                twist_candidate = set([i - j for i in time_candidate for j in move_clocks_time])
                for twist in twist_candidate:
                    search()




def solver(state):
    global solution
    for depth in range(13):
        solution = []
        search(depth, state, [set([]), set([])])
        judgenemt_state = [i for i in state]
        for pins, direction, twist in solution:
            judgenemt_state = move(judgenemt_state, pins, direction, twist)
        if set(judgenemt_state) == {0}:
            return solution





