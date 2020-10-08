# coding:utf-8
from itertools import combinations

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

def move(state, pins, direction, twist):
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
    return res_lower, res_upper, res_corner

def idx2state(idx_lower, idx_upper, idx_corner):
    res = [-1 for _ in range(14)]
    for i in [1, 3, 4, 5, 7]:
        res[i] = idx_upper % 12
        idx_upper //= 12
    for i in [9, 10, 11, 12, 13]:
        res[i] = idx_lower % 12
        idx_lower //= 12
    for i in [0, 2, 6, 8]:
        res[i] = idx_corner % 12
        idx_corner //= 12
    return res

grip_cost = 3

combs = []
for i in range(5):
    combs.append([j for j in combinations(range(4), i)])