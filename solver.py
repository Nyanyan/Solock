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
from collections import Counter

def distance(phase, state):
    lower_idx, upper_idx, corner_idx = state2idx(state)
    if phase == 0:
        return cross_cost[lower_idx], cross_cost[upper_idx]
    elif phase == 1:
        return cross_cost[upper_idx], corner_cost[corner_idx]
    else:
        return corner_cost[corner_idx], -1

'''
def optimise(sol):
    sol.sort()
    res = []
    idx = 0
    while idx < len(sol):
        pin, twist = sol[idx]
        r_idx = idx + 1
        while r_idx < len(sol) and sol[r_idx][0] == pin:
            r_idx += 1
        twist = sum([i[1] for i in sol[idx:r_idx]]) % 12
        if twist:
            res.append([pin, twist])
        idx = r_idx
    #print('opt', len(sol), len(res))
    return res
'''

def search(phase, depth, state, strt_idx):
    global solution
    solved_solution = []
    dis, _ = distance(phase, state)
    for idx, pin_num in enumerate(pins_num_candidate[phase][strt_idx:]):
        n_strt_idx = strt_idx + idx + 1
        pin_rev = pin_num - 1 if pin_num % 2 else pin_num + 1
        if pin_num in set_solution:
            continue
        #f_cost = -1
        #if pin_rev in set_solution:
        f_cost = calculate_cost(solution)
        for twist, twist_proc in zip(range(1, 12), [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]):
            #if f_cost == -1:
            n_depth = depth - grip_cost - twist_proc
            if n_depth < 0:
                continue
            n_state = move(state, pin_num, twist)
            n_dis, n_next_dis = distance(phase, n_state)
            if n_dis > dis:
                continue
            solution.append([pin_num, twist])
            #if f_cost >= 0:
            n_depth = depth - (calculate_cost(solution) - f_cost)
            if phase == 2:
                if n_dis == 0:
                    return [[[[i for i in j] for j in solution], 0]]
                if n_dis <= n_depth:
                    tmp = search(phase, n_depth, n_state, n_strt_idx)
                    if tmp:
                        return tmp
            else:
                if n_dis == 0:
                    solved_solution.append([[[i for i in j] for j in solution], n_next_dis])
                if n_dis <= n_depth:
                    tmp = search(phase, n_depth, n_state, n_strt_idx)
                    if tmp:
                        solved_solution.extend(tmp)
            solution.pop()
    return solved_solution

def separate_twist(twist_addition):
    if not twist_addition:
        return []
    res_now = []
    pls_pin = twist_addition[0][0]
    for idx, each_twist in enumerate(twist_addition):
        if each_twist[0] == pls_pin:
            res_now.append(each_twist)
        else:
            break
    n_twist_addition = [i for i in twist_addition[len(res_now):]]
    return_vals = separate_twist(n_twist_addition)
    if not return_vals:
        return [[i] for i in res_now]
    res = []
    for each_twist in res_now:
        res.append([each_twist])
        for return_val in return_vals:
            tmp = [[i for i in j] for j in return_val]
            tmp.append(each_twist)
            res.append(tmp)
    return res

def calculate_cost(sol):
    sol = [[i[0] // 2, i[1]] for i in sol]
    sol.sort()
    res = 0
    idx = 0
    while idx < len(sol):
        pin, twist = sol[idx]
        res += grip_cost
        f_twist = 0
        if idx < len(sol) - 1 and sol[idx + 1][0] == pin:
            f_twist = min(sol[idx + 1][1], abs(sol[idx + 1][1] - 12))
            idx += 1
        res += max(f_twist, min(twist, abs(twist - 12)))
        idx += 1
    return res

def solver_p(phase, state, pre_solution):
    global solution, set_solution
    dis_state, _ = distance(phase, state)
    # If you turn both layers (and the amount of twist is small), the cost does not increase much
    both_layer_twists = []
    for pin_num, f_twist in pre_solution:
        pin_rev = pin_num - 1 if pin_num % 2 else pin_num + 1
        if not pin_rev in set_pins_num_candidate[phase]:
            continue
        f_cost = min(f_twist, abs(f_twist - 12))
        min_dis = dis_state
        additional_twists = []
        for twist in range(1, 12):
            n_state = move(state, pin_rev, twist)
            n_dis, _ = distance(phase, n_state)
            if n_dis <= min_dis:
                if n_dis < min_dis:
                    additional_twists = []
                    min_dis = n_dis
                additional_twists.append([pin_rev, twist])
        both_layer_twists.extend(additional_twists)
    if phase == 2:
        for pin_num, pin_rev in [[14, 15], [16, 17]]:
            min_dis = dis_state
            additional_twists = []
            for twist_num in range(1, 12):
                for twist_rev in range(1, 12):
                    n_state = move(state, pin_num, twist_num)
                    n_state = move(n_state, pin_rev, twist_rev)
                    n_dis, _ = distance(phase, n_state)
                    if n_dis <= min_dis:
                        if n_dis < min_dis:
                            additional_twists = []
                            min_dis = n_dis
                        additional_twists.append([pin_num, twist_num])
                        additional_twists.append([pin_rev, twist_rev])
            both_layer_twists.extend(additional_twists)
    both_layer_twists.sort()
    twist_lsts = separate_twist(both_layer_twists)
    twist_lsts.append([])
    res = []
    #print(phase, len(twist_lsts))
    pre_cost = calculate_cost(pre_solution)
    for twist_lst in twist_lsts:
        n_state = [i for i in state]
        for pin_num, twist in twist_lst:
            n_state = move(n_state, pin_num, twist)
        solution = [[i for i in j] for j in pre_solution]
        #print(phase, twist_lst)
        #print('bef', phase, state, dis_state, pre_cost)
        solution.extend(twist_lst)
        solution.sort()
        twisted_cost = calculate_cost(solution)
        strt = len(solution)
        set_solution = set(i[0] for i in solution)
        depth, nn_cost = distance(phase, n_state)
        #print('aft', phase, n_state, depth, twisted_cost)
        if depth + twisted_cost > dis_state + pre_cost:
            #print('a')
            continue
        if depth == 0:
            res.append([twisted_cost, nn_cost, n_state, [[i for i in j] for j in solution]])
        searched_solutions = search(phase, depth, n_state, 0)
        if searched_solutions:
            for solution_candidate, n_cost in searched_solutions:
                nn_state = [i for i in n_state]
                for pin_num, twist in solution_candidate[strt:]:
                    nn_state = move(nn_state, pin_num, twist)
                res.append([twisted_cost + depth, n_cost, nn_state, solution_candidate])
    return res

def solver(state):
    cost = 0
    all_solution = []
    states = [[0, distance(0, state)[1], state, []]]
    n_states = []
    for phase in range(3):
        for _, _, state, phase_solution in states:
            n_states.extend(solver_p(phase, state, phase_solution))
        if phase == 0:
            states = deepcopy(n_states)
            n_states = []
        elif phase == 1:
            states = [deepcopy(n_states[0])]
            n_states = []
    result = [[calculate_cost(i[3]), i[3]] for i in n_states]
    result.sort()
    chosen_solution = result[0][1]
    chosen_cost = result[0][0]
    #print(chosen_solution)
    chosen_solution.sort()
    #print('chosen', chosen_solution)
    #print(calculate_cost(chosen_solution))
    chosen_solution_symbol = [[pins_candidate[i[0]][0], pins_candidate[i[0]][1], i[1]] for i in chosen_solution]
    return chosen_solution_symbol, chosen_cost

solution = []
set_solution = set()

with open('cross_cost.csv', mode='r') as f:
    cross_cost = [int(i) for i in f.readline().replace('\n', '').split(',')]
with open('corner_cost.csv', mode='r') as f:
    corner_cost = [int(i) for i in f.readline().replace('\n', '').split(',')]

print('solver initialized')

'''
from time import time

from random import randint
tims = []
lens = []
costs = []
scrambles = []
cnt = 0
num = 100 #100000
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

strt = time()
#tmp = solver([11, 10, 9, 9, 2, 1, 8, 7, 4, 1, 5, 0, 4, 1])
#tmp = solver([7, 10, 2, 1, 1, 5, 5, 4, 4, 5, 11, 8, 11, 5])
#tmp = solver([9, 9, 1, 8, 10, 11, 0, 11, 10, 7, 6, 4, 1, 8])
#tmp = solver([3, 10, 8, 0, 0, 3, 3, 6, 0, 1, 0, 2, 0, 1])
#tmp = solver([7, 5, 8, 10, 11, 5, 11, 4, 7, 4, 8, 2, 11, 6])
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
#tmp = solver([6, 3, 10, 2, 3, 5, 8, 5, 9, 4, 4, 6, 7, 6]) # UR6+ DR5+ DL3+ UL1+ U5+ R3+ D6+ L5- ALL6+ y2 U2- R1+ D0+ L2- ALL6+ DR UL
print(len(tmp[0]), tmp[0], tmp[1], time() - strt)
#print(solver([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 0]))
#print(solver([9, 3, 3, 0, 3, 3, 9, 0, 9, 3, 3, 3, 3, 3]))
'''