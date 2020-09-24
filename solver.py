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

solution = []

def search(phase, depth, state, banned_pins):
    global solution
    lower_cross = set([state[i] for i in [9, 10, 11, 12, 13]]) == {0}
    upper_cross = len(set([state[i] for i in [1, 3, 4, 5, 7]])) == 1
    upper = set([state[i] for i in [0, 2, 6, 8, 1, 3, 4, 5, 7]]) == {0}
    if depth == 0:
        if phase == 0:
            return lower_cross
        elif phase == 1:
            return upper_cross
        elif phase == 2:
            return lower_cross and upper_cross and upper
    direction = 0 if phase == 0 else 1
    if phase == 0:
        pin_candidate = range(4)
    elif phase == 1:
        pin_candidate = range(1, 5)
    elif phase == 2:
        pin_candidate = range(3, 5)
    for num_of_pins in pin_candidate: # pins that are pulled
        for pins_up in combinations(range(4), num_of_pins):
            pins = [True if i in pins_up else False for i in range(4)]
            if pins in banned_pins[direction]:
                continue
            move_clocks_time = [state[i] for i in y_move_clocks(pins, direction)]
            not_move_clocks = n_move_clocks(pins, direction)
            if phase == 0:
                not_move_clocks -= set([0, 2, 6, 8, 1, 3, 4, 5, 7])
            elif phase == 1:
                not_move_clocks -= set([0, 2, 6, 8, 9, 10, 11, 12, 13])
            elif phase == 2:
                not_move_clocks -= set([9, 10, 11, 12, 13])
            if not lower_cross or not upper_cross:
                not_move_clocks -=  set([0, 2, 6, 8])
            time_candidate = set([state[i] for i in not_move_clocks])
            if phase == 2 and len(set([state[i] for i in range(9)])) == 1:
                twist_candidate = set([-state[0] % 12])
            else:
                twist_candidate = set([(i - j) % 12 for i in time_candidate for j in move_clocks_time])
            for twist in twist_candidate:
                if twist == 0:
                    continue
                n_state = move(state, pins, direction, twist)
                n_banned_pins = [[i for i in j] for j in banned_pins]
                n_banned_pins[direction].append(pins)
                solution.append([pins, direction, twist])
                if search(phase, depth - 1, n_state, n_banned_pins):
                    return True
                solution.pop()
                #n_banned_pins[direction].pop()
    return False

def solver(state):
    global solution
    strt = 0
    solution = []
    for phase in range(3):
        for depth in range(6):
            if search(phase, depth, state, [[], []]):
                for pins, direction, twist in solution[strt:]:
                    state = move(state, pins, direction, twist)
                strt = len(solution)
                break
        else:
            return -1
    return solution

#test_cube = [3, 6, 0, 3, 6, 3, 0, 0, 0, 9, 9, 9, 0, 0]
test_cube = [5, 9, 6, 7, 9, 2, 8, 5, 1, 6, 9, 6, 0, 0] # UR1- DR2- DL5- UL0+ U5+ R5+ D5- L0+ ALL0+ y2 U6+ R3+ D0+ L6+ ALL3+
print(test_cube)
print(solver(test_cube))


