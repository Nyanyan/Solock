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

def distance(phase, state):
    lower_idx, upper_idx, corner_idx = state2idx(state)
    if phase == 0:
        return lower_cost[lower_idx]
    elif phase == 1:
        return upper_cost[upper_idx]
    elif phase == 2:
        return corner_cost[corner_idx]

def search(phase, depth, state, banned_pins):
    global solution
    dis = distance(phase, state)
    if depth <= 0:
        return dis == 0
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
                if n_dis > dis:
                    continue
                solution.append([pins, direction, twist])
                if n_dis <= n_depth:
                    if search(phase, n_depth, n_state, n_banned_pins):
                        return True
                solution.pop()
    return False

def solver(state):
    global solution
    strt = 0
    solution = []
    cost = 0
    for phase in range(3):
        for depth in range(50):
            if search(phase, depth, state, [[], []]):
                for pins, direction, twist in solution[strt:]:
                    state = move(state, pins, direction, twist)
                strt = len(solution)
                cost += depth
                break
        else:
            return -1, -1
    return solution, cost

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

'''
strt = time()
tmp = solver([5, 11, 6, 1, 4, 3, 5, 7, 1, 10, 5, 6, 11, 9])
print(len(tmp), tmp, time() - strt) # UR3- DR5- DL0+ UL3- U3+ R3- D1+ L2- ALL6+ y2 U3- R3+ D5+ L1+ ALL2- DR DL UL
#print(solver([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 0]))
#print(solver([9, 3, 3, 0, 3, 3, 9, 0, 9, 3, 3, 3, 3, 3]))
'''