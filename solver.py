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
        return cross_cost[lower_idx]
    else:
        return max(cross_cost[upper_idx], corner_cost[corner_idx])

cnt = 0
def search(phase, depth, state, banned_pins):
    global solution, cnt
    cnt += 1
    if cnt % 1000 == 0:
        print('    ', cnt)
    '''
    if phase == 0:
        set_clocks = set(state[i] for i in [9, 10, 11, 12, 13])
    elif phase == 1:
        set_clocks = set(state[i] for i in [0, 2, 6, 8, 1, 3, 4, 5, 7])
    '''
    dis = distance(phase, state)
    if depth <= 0:
        return dis == 0
    direction = phase
    pins_candidate = [range(4), range(1, 5)]
    for num_of_pins in pins_candidate[phase]: # pins that are pulled
        for pins_up in combs[num_of_pins]:
            pins = [True if i in pins_up else False for i in range(4)]
            if pins in banned_pins[direction]:
                continue
            '''
            move_clocks = move_clocks_p(pins, direction)
            move_clocks_time = [state[i] for i in move_clocks]
            not_move_clocks = set(range(14)) - move_clocks
            if phase == 0:
                not_move_clocks -= {0, 2, 6, 8, 1, 3, 4, 5, 7}
            elif phase == 1:
                not_move_clocks -= {9, 10, 11, 12, 13}
            time_candidate = set(state[i] for i in not_move_clocks)
            if phase == 1:
                twist_candidate = set((i - j) % 12 for i in time_candidate for j in move_clocks_time)
            elif phase == 0:
                if len(set_clocks) == 1:
                    twist_candidate = set([-state[9] % 12])
                else:
                    twist_candidate = set((j - i) % 12 for i in time_candidate for j in move_clocks_time)
            twist_candidate = sorted(list(twist_candidate))
            '''
            twist_candidate = range(1, 12)
            n_banned_pins = [[i for i in j] for j in banned_pins]
            n_banned_pins[direction].append(pins)
            for twist in twist_candidate:
                '''
                if twist == 0:
                    continue
                '''
                n_state = move(state, pins, direction, twist)
                '''
                if phase == 0:
                    n_set_clocks = set(n_state[i] for i in [9, 10, 11, 12, 13])
                elif phase == 1:
                    n_set_clocks = set(n_state[i] for i in [1, 3, 4, 5, 7])
                elif phase == 2:
                    n_set_clocks = set(n_state[i] for i in [0, 2, 6, 8, 1, 3, 4, 5, 7])
                if len(n_set_clocks) <= depth:
                    if search(phase, depth - 1, n_state, n_banned_pins):
                        return True
                '''
                twist_proc = twist if twist <= 6 else 12 - twist
                n_depth = depth - grip_cost - twist_proc
                n_dis = distance(phase, n_state)
                if n_dis > dis:
                    continue
                solution.append([pins, direction, twist])
                if phase == 1 and n_dis <= 
                if n_dis <= n_depth:
                    if search(phase, n_depth, n_state, n_banned_pins):
                        return True
                solution.pop()
                #n_banned_pins[direction].pop()
    return False

def solver(state):
    global solution
    strt = 0
    solution = []
    for phase in range(2):
        for depth in range(100):
            print(depth)
            if search(phase, depth, state, [[], []]):
                for pins, direction, twist in solution[strt:]:
                    state = move(state, pins, direction, twist)
                strt = len(solution)
                #print(phase)
                print(solution)
                break
        else:
            return -1
    return solution

solution = []

with open('cross_cost.csv', mode='r') as f:
    cross_cost = [int(i) for i in f.readline().replace('\n', '').split(',')]
with open('corner_cost.csv', mode='r') as f:
    corner_cost = [int(i) for i in f.readline().replace('\n', '').split(',')]

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
print(solver([5, 11, 6, 1, 4, 3, 5, 7, 1, 10, 5, 6, 11, 9])) # UR3- DR5- DL0+ UL3- U3+ R3- D1+ L2- ALL6+ y2 U3- R3+ D5+ L1+ ALL2- DR DL UL
#print(solver([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 0]))
#print(solver([9, 3, 3, 0, 3, 3, 9, 0, 9, 3, 3, 3, 3, 3]))