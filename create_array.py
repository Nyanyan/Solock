# coding:utf-8
from collections import deque
import csv
from copy import deepcopy

from basic_functions import *

def create_cross_cost():
    cross_cost = [1000 for _ in range(12 ** 5)] # 5 clocks that form the cross
    solved = [[i for _ in range(14)] for i in range(12)]
    for i in range(12):
        cross_cost[state2idx(solved[i])[1]] = 0
    que = deque([[solved[i], 0] for i in range(12)])
    cnt = 0
    phase = 1
    while que:
        cnt += 1
        if cnt % 1000 == 0:
            print(cnt, len(que))
        '''
        state, cost, pins, pin_twist = que.popleft()
        for pin_num in pins_num_candidate[phase]:
            if pin_num in pins:
                continue
            n_pin_num = pin_num - 1 if pin_num % 2 else pin_num + 1
            former_twist = 0
            if n_pin_num in pins:
                former_twist = pin_twist[n_pin_num]
                n_cost_base = cost - former_twist
            else:
                n_cost_base = cost + grip_cost
            n_pins = {i for i in pins}
            n_pins.add(pin_num)
            for twist in range(1, 12):
                n_state = move(state, pin_num, twist)
                n_idx = state2idx(n_state)[phase]
                twist_proc = min(twist, abs(12 - twist))
                n_cost = n_cost_base + max(twist_proc, former_twist)
                n_pin_twist = deepcopy(pin_twist)
                n_pin_twist[pin_num] = twist_proc
                if cross_cost[n_idx] > n_cost:
                    cross_cost[n_idx] = n_cost
                    que.append([n_state, n_cost, n_pins, n_pin_twist])
        '''
        state, cost = que.popleft()
        for pin_num in pins_num_candidate[phase]:
            for twist in range(1, 12):
                n_state = move(state, pin_num, twist)
                n_idx = state2idx(n_state)[phase]
                n_cost = cost + grip_cost + min(twist, abs(12 - twist))
                if cross_cost[n_idx] > n_cost:
                    cross_cost[n_idx] = n_cost
                    que.append([n_state, n_cost])
    with open('cross_cost.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(cross_cost)

def create_corner_cost():
    corner_cost = [1000 for _ in range(12 ** 6)] # 4 clocks that form corners and 2 direction of cross clocks
    solved = [0 for _ in range(14)]
    corner_cost[state2idx(solved)[2]] = 0
    que = deque([[solved, 0]])
    cnt = 0
    phase = 2
    while que:
        cnt += 1
        if cnt % 1000 == 0:
            print(cnt, len(que))
        '''
        state, cost, pins, pin_twist = que.popleft()
        for pin_num in pins_num_candidate[phase]:
            if pin_num in pins:
                continue
            n_pin_num = pin_num - 1 if pin_num % 2 else pin_num + 1
            former_twist = 0
            if n_pin_num in pins:
                former_twist = pin_twist[n_pin_num]
                n_cost_base = cost - former_twist
            else:
                n_cost_base = cost + grip_cost
            n_pins = {i for i in pins}
            n_pins.add(pin_num)
            for twist in range(1, 12):
                n_state = move(state, pin_num, twist)
                n_idx = state2idx(n_state)[phase]
                twist_proc = min(twist, abs(12 - twist))
                n_cost = n_cost_base + max(twist_proc, former_twist)
                n_pin_twist = deepcopy(pin_twist)
                n_pin_twist[pin_num] = twist_proc
                if corner_cost[n_idx] > n_cost:
                    corner_cost[n_idx] = n_cost
                    que.append([n_state, n_cost, n_pins, n_pin_twist])
        '''
        state, cost = que.popleft()
        for pin_num in pins_num_candidate[phase]:
            for twist in range(1, 12):
                n_state = move(state, pin_num, twist)
                n_idx = state2idx(n_state)[phase]
                n_cost = cost + grip_cost + min(twist, abs(12 - twist))
                if corner_cost[n_idx] > n_cost:
                    corner_cost[n_idx] = n_cost
                    que.append([n_state, n_cost])
    with open('corner_cost.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(corner_cost)

create_cross_cost()
#create_corner_cost()
