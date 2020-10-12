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
        return cross_cost[lower_idx], cross_cost[upper_idx]
    elif phase == 1:
        return cross_cost[upper_idx], corner_cost[corner_idx]
    else:
        return corner_cost[corner_idx], -1

'''
def depth_0_search(phase, state):
    global solution
    n_dis, n_next_dis = distance(phase, state)
    nn_state = [i for i in state]
    for f_pin_num, f_twist in solution:
        nn_pin_num = f_pin_num - 1 if f_pin_num % 2 else f_pin_num + 1
        if nn_pin_num in set([i[0] for i in solution]) or not nn_pin_num in pins_num_candidate[phase]:
            continue
        f_twist_proc = min(f_twist, abs(12 - f_twist))
        nn_twists = list(range(1, f_twist_proc + 1))
        nn_twists.extend(list(range(12 - f_twist_proc, 12)))
        for nn_twist in nn_twists:
            nn_state = move(nn_state, nn_pin_num, nn_twist)
            nn_dis, nn_next_dis = distance(phase, nn_state)
            if nn_dis >= n_dis:
                continue
            solution.append([nn_pin_num, nn_twist])
            if nn_dis == 0:
                print('bbbbbbbbbb')
                return nn_dis, nn_next_dis
            nnn_dis, nnn_next_dis = depth_0_search(phase, nn_state)
            if nnn_dis == 0:
                return nnn_dis, nnn_next_dis
            solution.pop()
    return n_dis, n_next_dis
'''

def search(phase, depth, state, strt_idx, solution_strt):
    global solution
    solved_solution = []
    dis, _ = distance(phase, state)
    pins_solution = [i[0] for i in solution]
    set_solution = set(pins_solution)
    for idx, pin_num in enumerate(pins_num_candidate[phase][strt_idx:]): # to find normal solution
        n_pin_num = pin_num - 1 if pin_num % 2 else pin_num + 1
        former_twist = 0
        if n_pin_num in set_solution: # to find faster solution: search the solution in which the robot twist the both layer
            former_twist = solution[pins_solution.index(n_pin_num)][1]
            n_depth_base = depth + former_twist
        else:
            n_depth_base = depth - grip_cost
        if n_depth_base < 0:
            continue
        n_strt_idx = strt_idx + idx + 1
        for twist in range(1, 12):
            twist_proc = min(twist, abs(12 - twist))
            n_depth = n_depth_base - max(former_twist, twist_proc)
            if n_depth < 0:
                continue
            n_state = move(state, pin_num, twist)
            n_dis, n_next_dis = distance(phase, n_state)
            if n_dis + depth > dis + n_depth:
                continue
            solution.append([pin_num, twist])
            if phase == 2:
                if n_dis == 0:
                    return [[[[i for i in j] for j in solution], 0]]
                # Although the depth is 0, if you turn both layers (and the amount of twist is small), the cost does not increase
                if n_dis <= n_depth + len(solution[solution_strt:]) * grip_cost + sum([max(i[1], abs(12 - i[1])) for i in solution[solution_strt:]]):
                    tmp = search(phase, n_depth, n_state, n_strt_idx, solution_strt)
                    if tmp:
                        return tmp
            else:
                if n_dis == 0:
                    solved_solution.append([[[i for i in j] for j in solution], n_next_dis])
                # Although the depth is 0, if you turn both layers (and the amount of twist is small), the cost does not increase
                if n_dis <= n_depth + len(solution[solution_strt:]) * grip_cost + sum([max(i[1], abs(12 - i[1])) for i in solution[solution_strt:]]):
                    tmp = search(phase, n_depth, n_state, n_strt_idx, solution_strt)
                    if tmp:
                        solved_solution.extend(tmp)
            solution.pop()
    return solved_solution

def solver_p(phase, state, pre_solution, pre_cost):
    global solution
    dis, n_dis = distance(phase, state)
    #print(dis)
    strt = len(pre_solution)
    res = []
    #print(state)
    for depth in range(dis + 1):
        solution = [[i for i in j] for j in pre_solution]
        #print(phase, depth)
        solutions = search(phase, depth, state, 0, len(solution))
        if solutions:
            #solutions.sort(key=lambda x: x[1] + x[2])
            #print(len(solutions))
            #print(phase, depth)
            states = []
            for solution_candidate, n_next_cost in solutions:
                n_state = [i for i in state]
                for pin_num, twist in solution_candidate[strt:]:
                    n_state = move(n_state, pin_num, twist)
                states.append(n_state)
                res.append([pre_cost + depth, n_next_cost, n_state, solution_candidate])
            break
    #print('done', phase, len(res))
    #print(res[0])
    #res.sort(key=lambda x:x[0] + x[1])
    return res

def solver(state):
    cost = 0
    all_solution = []
    states = [[0, distance(0, state)[1], state, []]]
    n_states = []
    for phase in range(3):
        for cost, _, state, phase_solution in states:
            n_states.extend(solver_p(phase, state, phase_solution, cost))
        n_states.sort(key=lambda x: x[0] + x[1])
        if phase == 0:
            states = deepcopy(n_states[:min(len(n_states), 5)])
            n_states = []
        elif phase == 1:
            states = [deepcopy(n_states[0])]
            n_states = []
    chosen_solution = n_states[0][3]
    chosen_cost = n_states[0][0]
    #print(chosen_solution)
    chosen_solution.sort()
    chosen_solution_symbol = [[pins_candidate[i[0]][0], pins_candidate[i[0]][1], i[1]] for i in chosen_solution]
    return chosen_solution_symbol, chosen_cost

solution = []

with open('cross_cost.csv', mode='r') as f:
    cross_cost = [int(i) for i in f.readline().replace('\n', '').split(',')]
with open('corner_cost.csv', mode='r') as f:
    corner_cost = [int(i) for i in f.readline().replace('\n', '').split(',')]

print('solver initialized')


from time import time

from random import randint
tims = []
lens = []
costs = []
scrambles = []
cnt = 0
num = 50 #100000
for i in range(num):
    strt = time()
    test_cube = [randint(0, 11) for _ in range(14)]
    with open('log.txt', mode='a') as f:
        f.write(str(test_cube) + '\n')
    res, cost = solver(test_cube)
    tim = time() - strt
    print(i, len(res), 'moves', cost, 'cost', tim, 'sec')
    tims.append(tim)
    lens.append(len(res))
    costs.append(cost)
    scrambles.append(test_cube)
    cnt += 1
print(cnt, '/', num)
print('avg', sum(tims) / cnt, 'sec', 'max', max(tims), 'sec')
print('avg', sum(lens) / cnt, 'moves', 'max', max(lens), 'moves')
print('avg', sum(costs) / cnt, 'cost', 'max', max(costs), 'cost')
print('longest time scramble', scrambles[tims.index(max(tims))])
'''
strt = time()
#tmp = solver([11, 10, 6, 4, 4, 2, 11, 2, 3, 3, 7, 6, 7, 4])
#tmp = solver([8, 2, 2, 8, 6, 4, 2, 9, 2, 6, 10, 5, 0, 4])
#tmp = solver([10, 2, 8, 4, 8, 1, 2, 2, 7, 3, 9, 1, 10, 3])
#tmp = solver([0, 2, 3, 1, 6, 1, 8, 11, 5, 10, 1, 3, 11, 0])
#tmp = solver([11, 9, 7, 1, 3, 4, 7, 8, 5, 1, 3, 0, 9, 5])
#tmp = solver([0, 9, 11, 11, 7, 1, 1, 5, 4, 2, 0, 10, 9, 3])
#tmp = solver([2, 9, 5, 11, 0, 4, 9, 6, 4, 3, 9, 10, 7, 6])
#tmp = solver([6, 3, 1, 3, 3, 3, 7, 3, 6, 6, 8, 1, 9, 2]) # skip
#tmp = solver([6, 7, 10, 9, 1, 4, 5, 1, 7, 2, 1, 2, 2, 10])
#tmp = solver([5, 11, 6, 1, 4, 3, 5, 7, 1, 10, 5, 6, 11, 9]) # UR3- DR5- DL0+ UL3- U3+ R3- D1+ L2- ALL6+ y2 U3- R3+ D5+ L1+ ALL2- DR DL UL
tmp = solver([6, 3, 10, 2, 3, 5, 8, 5, 9, 4, 4, 6, 7, 6]) # UR6+ DR5+ DL3+ UL1+ U5+ R3+ D6+ L5- ALL6+ y2 U2- R1+ D0+ L2- ALL6+ DR UL
print(len(tmp[0]), tmp[0], tmp[1], time() - strt)
#print(solver([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 0]))
#print(solver([9, 3, 3, 0, 3, 3, 9, 0, 9, 3, 3, 3, 3, 3]))
'''