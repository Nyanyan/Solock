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

def search(phase, depth, state, num_pin, strt_pin, cost):
    global solution
    solved_solution = []
    dis = distance(phase, state)
    direction = int(bool(phase))
    pins_candidate = [[0, 1, 2, 3], [1, 2], [2, 3, 4]]
    for twist in range(1, 12):
        twist_proc = twist if twist <= 6 else 12 - twist
        n_depth = depth - grip_cost - twist_proc
        for idx_num_pins, num_of_pins in enumerate(pins_candidate[phase][num_pin:]): # pins that are pulled
            n_num_pin = idx_num_pins
            cmbs_proc = combs[num_of_pins][strt_pin:] if idx_num_pins == num_pin else combs[num_of_pins]
            for idx_pins_up, pins_up in enumerate(cmbs_proc):
                pins = [True if i in pins_up else False for i in range(4)]
                if phase == 2 and num_of_pins == 2 and not pins in [[True, False, True, False], [False, True, True, False]]:
                    continue
                n_strt_pin = idx_pins_up + 1
                n_state = move(state, pins, direction, twist)
                n_dis = distance(phase, n_state)
                n_cost = cost + grip_cost + twist_proc
                if n_dis > dis:
                    continue
                solution.append([pins, direction, twist])
                if n_dis == 0:
                    solved_solution.append([deepcopy(solution), n_cost])
                elif n_dis <= n_depth:
                    tmp = search(phase, n_depth, n_state, n_num_pin, n_strt_pin, n_cost)
                    if len(tmp):
                        solved_solution.extend(tmp)
                if len(solved_solution) >= 2:
                    return solved_solution
                solution.pop()
    return solved_solution

def solver_p(phase, state, pre_solution, pre_cost):
    global solution
    if distance(phase, state) == 0:
        return [pre_cost, state, pre_solution]
    admissible_depth = 0
    res = []
    for depth in range(40):
        solution = deepcopy(pre_solution)
        #print(phase, depth)
        phase_solutions = search(phase, depth + admissible_depth, state, 0, 0, pre_cost)
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


from time import time
from random import randint
tims = []
lens = []
costs = []
scrambles = []
cnt = 0
num = 100
for i in range(num):
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
        scrambles.append(test_cube)
        cnt += 1
print(cnt, '/', num)
print('avg', sum(tims) / cnt, 'sec', 'max', max(tims), 'sec')
print('avg', sum(lens) / cnt, 'moves', 'max', max(lens), 'moves')
print('avg', sum(costs) / cnt, 'cost', 'max', max(costs), 'cost')
print(scrambles[tims.index(max(tims))])

'''
strt = time()
tmp = solver([2, 11, 7, 11, 6, 6, 11, 8, 9, 2, 3, 1, 3, 6])
#tmp = solver([5, 11, 6, 1, 4, 3, 5, 7, 1, 10, 5, 6, 11, 9])
print(len(tmp[0]), tmp[0], tmp[1], time() - strt) # UR3- DR5- DL0+ UL3- U3+ R3- D1+ L2- ALL6+ y2 U3- R3+ D5+ L1+ ALL2- DR DL UL
#print(solver([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 0]))
#print(solver([9, 3, 3, 0, 3, 3, 9, 0, 9, 3, 3, 3, 3, 3]))
'''