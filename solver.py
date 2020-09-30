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

solved: state == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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
    return set(res)

def n_move_clocks(pins, direction):
    res = set(range(14)) - y_move_clocks(pins, direction)
    return res

def move(state, pins, direction, twist):
    move_clocks = y_move_clocks(pins, direction)
    res = [i for i in state]
    for i in move_clocks:
        if direction or i in {0, 2, 6, 8}:
            res[i] += twist
        else:
            res[i] -= twist
        res[i] %= 12
    return res

solution = []

def search(phase, depth, state, banned_pins):
    global solution
    if phase == 0:
        set_clocks = set(state[i] for i in [9, 10, 11, 12, 13])
    elif phase == 1:
        set_clocks = set(state[i] for i in [1, 3, 4, 5, 7])
    elif phase == 2:
        set_clocks = set(state[i] for i in [0, 2, 6, 8, 1, 3, 4, 5, 7])
    if depth == 0:
        if phase == 0 or phase == 2:
            return set_clocks == {0}
        elif phase == 1:
            return len(set_clocks) == 1
    direction = 0 if phase == 0 else 1
    if phase == 0:
        pin_candidate = [1, 2, 3]
    elif phase == 1:
        pin_candidate = [1, 2]
    elif phase == 2:
        pin_candidate = [3, 4]
    for num_of_pins in pin_candidate: # pins that are pulled
        for pins_up in combs[num_of_pins]:
            pins = [True if i in pins_up else False for i in range(4)]
            if pins in banned_pins[direction] or (phase == 2 and num_of_pins == 2 and not pins_up in [[0, 3], [1, 2]]):
                continue
            move_clocks = y_move_clocks(pins, direction)
            move_clocks_time = [state[i] for i in move_clocks]
            not_move_clocks = set(range(14)) - move_clocks
            if phase == 0:
                not_move_clocks -= {0, 2, 6, 8, 1, 3, 4, 5, 7}
            elif phase == 1:
                not_move_clocks -= {0, 2, 6, 8, 9, 10, 11, 12, 13}
            elif phase == 2:
                not_move_clocks -= {9, 10, 11, 12, 13}
            time_candidate = set(state[i] for i in not_move_clocks)
            if phase == 2:
                if len(set_clocks) == 1:
                    twist_candidate = set([-state[0] % 12])
                else:
                    twist_candidate = set((i - state[list(move_clocks)[0]]) % 12 for i in time_candidate) - {0}
            elif phase == 1:
                twist_candidate = set((i - j) % 12 for i in time_candidate for j in move_clocks_time)
            elif phase == 0:
                if len(set_clocks) == 1:
                    twist_candidate = set([-state[9] % 12])
                else:
                    twist_candidate = set((j - i) % 12 for i in time_candidate for j in move_clocks_time)
            for twist in twist_candidate:
                if twist == 0:
                    continue
                n_state = move(state, pins, direction, twist)
                n_banned_pins = [[i for i in j] for j in banned_pins]
                n_banned_pins[direction].append(pins)
                solution.append([pins, direction, twist])
                if phase == 0:
                    n_set_clocks = set(n_state[i] for i in [9, 10, 11, 12, 13])
                elif phase == 1:
                    n_set_clocks = set(n_state[i] for i in [1, 3, 4, 5, 7])
                elif phase == 2:
                    n_set_clocks = set(n_state[i] for i in [0, 2, 6, 8, 1, 3, 4, 5, 7])
                if len(n_set_clocks) <= depth:
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
                #print(phase)
                break
        else:
            return -1
    return solution

combs = []
for i in range(5):
    combs.append([j for j in combinations(range(4), i)])

'''
from time import time
from random import randint
tims = []
cnt = 0
num = 100
for _ in range(num):
    strt = time()
    test_cube = [randint(0, 11) for _ in range(14)]
    res = solver(test_cube)
    if res != -1:
        print(len(res), 'moves')
        tim = time() - strt
        print(tim, 'sec')
        tims.append(tim)
        cnt += 1
print(cnt, '/', num, 'avg', sum(tims) / cnt, 'sec', 'max', max(tims), 'sec')
'''
#print(solver([5, 11, 6, 1, 4, 3, 5, 7, 1, 10, 5, 6, 11, 9])) # UR3- DR5- DL0+ UL3- U3+ R3- D1+ L2- ALL6+ y2 U3- R3+ D5+ L1+ ALL2- DR DL UL
#print(solver([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 0]))
#print(solver([9, 3, 3, 0, 3, 3, 9, 0, 9, 3, 3, 3, 3, 3]))