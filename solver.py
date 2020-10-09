# coding:utf-8
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

from basic_functions import *
from copy import deepcopy

def distance(phase, state):
    lower_idx, upper_idx, corner_idx = state2idx(state)
    if phase == 0:
        return lower_cost[lower_idx]
    elif phase == 1:
        return upper_cost[upper_idx]
    elif phase == 2:
        return corner_cost[corner_idx]

def search(phase, depth, state, banned_pins, cost):
    global solution
    solved_solution = []
    dis = distance(phase, state)
    if dis == 0:
        return [[[], 0]]
    direction = int(bool(phase))
    pins_candidate = [[0, 1, 2, 3], [1, 2], [3, 4]]
    for num_of_pins in pins_candidate[phase]: # pins that are pulled
        for pins_up in combs[num_of_pins]:
            pins = [True if i in pins_up else False for i in range(4)]
            if pins in banned_pins[direction]:
                continue
            twist_candidate = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            n_banned_pins = [[i for i in j] for j in banned_pins]
            n_banned_pins[direction].append(pins)
            for twist in twist_candidate:
                n_state = move(state, pins, direction, twist)
                twist_proc = twist if twist <= 6 else 12 - twist
                n_depth = depth - grip_cost - twist_proc
                n_dis = distance(phase, n_state)
                n_cost = cost + grip_cost + twist_proc
                if n_dis > dis:
                    continue
                solution.append([pins, direction, twist])
                if n_dis == 0:
                    solved_solution.append([deepcopy(solution), n_cost])
                elif n_dis <= n_depth:
                    tmp = search(phase, n_depth, n_state, n_banned_pins, n_cost)
                    if len(tmp):
                        solved_solution.extend(tmp)
                if len(solved_solution) >= 1:
                    return solved_solution
                solution.pop()
    return solved_solution

def solver_p(phase, state, pre_solution, pre_cost):
    global solution
    admissible_depth = 0
    res = []
    for depth in range(50):
        solution = deepcopy(pre_solution)
        phase_solutions = search(phase, depth + admissible_depth, state, [[], []], pre_cost)
        if len(phase_solutions):
            for phase_solution, cost in phase_solutions:
                n_state = [i for i in state]
                for pins, direction, twist in phase_solution:
                    n_state = move(n_state, pins, direction, twist)
                res.append([cost, n_state, phase_solution])
            break
    #print(phase, len(res))
    return res

def solver(state):
    cost = 0
    all_solution = []
    states = [[0, state, []]]
    n_states = []
    for phase in range(3):
        for cost, state, phase_solution in states:
            n_states.extend(solver_p(phase, state, phase_solution, cost))
        states = deepcopy(n_states)
        n_states = []
    states.sort()
    chosen_solution = states[0][2]
    chosen_cost = states[0][0]
    return chosen_solution, chosen_cost

solution = []

with open('lower_cost.csv', mode='r') as f:
    lower_cost = [int(i) for i in f.readline().replace('\n', '').split(',')]
with open('upper_cost.csv', mode='r') as f:
    upper_cost = [int(i) for i in f.readline().replace('\n', '').split(',')]
with open('corner_cost.csv', mode='r') as f:
    corner_cost = [int(i) for i in f.readline().replace('\n', '').split(',')]

'''
from time import time
from random import randint
tims = []
lens = []
costs = []
cnt = 0
num = 100
for _ in range(num):
    strt = time()
    test_cube = [randint(0, 11) for _ in range(14)]
    res, cost = solver(test_cube)
    if res != -1:
        #print(len(res), 'moves')
        tim = time() - strt
        #print(tim, 'sec')
        tims.append(tim)
        lens.append(len(res))
        costs.append(cost)
        cnt += 1
print(cnt, '/', num)
print('avg', sum(tims) / cnt, 'sec', 'max', max(tims), 'sec')
print('avg', sum(lens) / cnt, 'moves', 'max', max(lens), 'moves')
print('avg', sum(costs) / cnt, 'cost', 'max', max(costs), 'cost')


strt = time()
tmp = solver([5, 11, 6, 1, 4, 3, 5, 7, 1, 10, 5, 6, 11, 9])
print(len(tmp[0]), tmp[0], tmp[1], time() - strt) # UR3- DR5- DL0+ UL3- U3+ R3- D1+ L2- ALL6+ y2 U3- R3+ D5+ L1+ ALL2- DR DL UL
#print(solver([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 0]))
#print(solver([9, 3, 3, 0, 3, 3, 9, 0, 9, 3, 3, 3, 3, 3]))
'''