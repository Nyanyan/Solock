# coding:utf-8

def move_clocks_p(pins, direction):
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

def move(state, num, twist):
    pins, direction = pins_candidate[num]
    move_clocks = move_clocks_p(pins, direction)
    res = [i for i in state]
    for i in move_clocks:
        if direction or i in {0, 2, 6, 8}:
            res[i] += twist
        else:
            res[i] -= twist
        res[i] %= 12
    return res

def state2idx(state):
    state_upper = [state[i] for i in [1, 3, 4, 5, 7]]
    state_lower = [state[i] for i in [9, 10, 11, 12, 13]]
    state_corner = [state[i] for i in [0, 2, 6, 8]]
    res_upper = 0
    for i in range(5):
        res_upper *= 12
        res_upper += state_upper[i]
    res_lower = 0
    for i in range(5):
        res_lower *= 12
        res_lower += state_lower[i]
    res_corner = 0
    for i in range(4):
        res_corner *= 12
        res_corner += state_corner[i]
    res_corner *= 12
    res_corner += state[1]
    res_corner *= 12
    res_corner += state[9]
    return res_lower, res_upper, res_corner

def idx2state(idx_lower, idx_upper, idx_corner):
    res = [-1 for _ in range(14)]
    for i in [1, 3, 4, 5, 7]:
        res[i] = idx_upper % 12
        idx_upper //= 12
    for i in [9, 10, 11, 12, 13]:
        res[i] = idx_lower % 12
        idx_lower //= 12
    res_corner //= 12 ** 2
    for i in [0, 2, 6, 8]:
        res[i] = idx_corner % 12
        idx_corner //= 12
    return res

grip_cost = 3

pins_candidate = [
    [[False, False, False, False], 0], [[False, False, False, False], 1],
    [[True, False, False, False], 0], [[True, False, False, False], 1], [[False, True, False, False], 0], [[False, True, False, False], 1], [[False, False, True, False], 0], [[False, False, True, False], 1], [[False, False, False, True], 0], [[False, False, False, True], 1], 
    [[True, True, False, False], 0], [[True, True, False, False], 1], [[True, False, True, False], 0], [[True, False, True, False], 1], [[True, False, False, True], 0], [[True, False, False, True], 1], [[False, True, True, False], 0], [[False, True, True, False], 1], [[False, True, False, True], 0], [[False, True, False, True], 1], [[False, False, True, True], 0], [[False, False, True, True], 1], 
    [[True, True, True, False], 0], [[True, True, True, False], 1], [[True, True, False, True], 0], [[True, True, False, True], 1], [[True, False, True, True], 0], [[True, False, True, True], 1], [[False, True, True, True], 0], [[False, True, True, True], 1], 
    [[True, True, True, True], 0], [[True, True, True, True], 1]
    ]

pins_num_candidate = [[10, 12, 18, 20, 22, 24, 26, 28], [3, 5, 7, 9, 11, 13, 19, 21], [0, 2, 4, 6, 8, 14, 16, 15, 16, 23, 25, 27, 29, 31]]
set_pins_num_candidate = [set(i) for i in pins_num_candidate]

print('basic functions initialized')

'''
pins_candidate_phase = [
    [[[True, True, False, False], 0], [[True, False, True, False], 0], [[False, True, False, True], 0], [[False, False, True, True], 0], [[True, True, True, False], 0], [[True, True, False, True], 0], [[True, False, True, True], 0], [[False, True, True, True], 0]],
    [[[True, False, False, False], 1], [[False, True, False, False], 1], [[False, False, True, False], 1], [[False, False, False, True], 1], [[True, True, False, False], 1], [[True, False, True, False], 1], [[False, True, False, True], 1], [[False, False, True, True], 1]],
    [
        [[False, False, False, False], 0], [[True, False, False, False], 0], [[False, True, False, False], 0], [[False, False, True, False], 0], [[False, False, False, True], 0], [[True, False, False, True], 0], [[False, True, True, False], 0],
        [[True, False, False, True], 1], [[False, True, True, False], 0], [[True, True, True, False], 1], [[True, True, False, True], 1], [[True, False, True, True], 1], [[False, True, True, True], 1], [[True, True, True, True], 1]
    ]
    ]
pins_num_candidate = [[], [], []]
for phase in range(3):
    for pins in pins_candidate_phase[phase]:
        pins_num_candidate[phase].append(pins_candidate.index(pins))

print(pins_num_candidate)
'''
'''
direction = [0, 1, 0]
for phase in range(3):
    for i in range(len(pins_candidate[phase])):
        pins_candidate[phase][i] = [pins_candidate[phase][i], direction[phase]]
for i in range(3):
    print(pins_candidate[i])
'''
'''
from itertools import combinations
combs = []
for i in range(5):
    combs.append([j for j in combinations(range(4), i)])

pins_up_candidate = [[2, 3], [1, 2], [0, 1, 2, 3, 4]]
pins_candidate = []
for num_of_pins in range(5):
    for pins_up in combs[num_of_pins]:
        for direction in range(2):
            pins_candidate.append([[True if i in pins_up else False for i in range(4)], direction])
print(pins_candidate)
'''