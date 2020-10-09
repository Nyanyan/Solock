# coding:utf-8
from collections import deque
import csv

from basic_functions import *

def create_lower_cost():
    lower_cost = [1000 for _ in range(12 ** 5)]
    solved = [0 for _ in range(14)]
    lower_cost[state2idx(solved)[0]] = 0
    que = deque([[solved, 0]])
    cnt = 0
    while que:
        state, cost = que.popleft()
        for num_of_pins in range(4):
            for pins_up in combs[num_of_pins]:
                pins = [True if i in pins_up else False for i in range(4)]
                for twist in range(1, 12):
                    n_state = move(state, pins, 0, twist)
                    n_idx = state2idx(n_state)[0]
                    twist_proc = twist if twist <= 6 else 12 - twist
                    n_cost = cost + grip_cost + twist_proc
                    if lower_cost[n_idx] > n_cost:
                        lower_cost[n_idx] = n_cost
                        que.append([n_state, n_cost])
                        cnt += 1
                        if cnt % 1000 == 0:
                            print(cnt, len(que))
    with open('lower_cost.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(lower_cost)

def create_upper_cost():
    upper_cost = [1000 for _ in range(12 ** 5)]
    solved = [[i for _ in range(14)] for i in range(12)]
    for i in range(12):
        upper_cost[state2idx(solved[i])[1]] = 0
    que = deque([[solved[i], 0] for i in range(12)])
    cnt = 0
    while que:
        state, cost = que.popleft()
        for num_of_pins in range(4):
            for pins_up in combs[num_of_pins]:
                pins = [True if i in pins_up else False for i in range(4)]
                for twist in range(1, 12):
                    n_state = move(state, pins, 1, twist)
                    n_idx = state2idx(n_state)[1]
                    twist_proc = twist if twist <= 6 else 12 - twist
                    n_cost = cost + grip_cost + twist_proc
                    if upper_cost[n_idx] > n_cost:
                        upper_cost[n_idx] = n_cost
                        que.append([n_state, n_cost])
                        cnt += 1
                        if cnt % 1000 == 0:
                            print(cnt, len(que))
    with open('upper_cost.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(upper_cost)

def create_corner_cost():
    corner_cost = [1000 for _ in range(12 ** 5)]
    solved = [0 for _ in range(14)]
    corner_cost[state2idx(solved)[2]] = 0
    que = deque([[solved, 0]])
    cnt = 0
    while que:
        state, cost = que.popleft()
        for num_of_pins in [3, 4]:
            for pins_up in combs[num_of_pins]:
                pins = [True if i in pins_up else False for i in range(4)]
                for twist in range(1, 12):
                    n_state = move(state, pins, 1, twist)
                    n_idx = state2idx(n_state)[2]
                    twist_proc = twist if twist <= 6 else 12 - twist
                    n_cost = cost + grip_cost + twist_proc
                    if corner_cost[n_idx] > n_cost:
                        corner_cost[n_idx] = n_cost
                        que.append([n_state, n_cost])
                        cnt += 1
                        if cnt % 1000 == 0:
                            print(cnt, len(que))
    with open('corner_cost.csv', mode='w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(corner_cost)

#create_lower_cost()
#create_upper_cost()
create_corner_cost()
