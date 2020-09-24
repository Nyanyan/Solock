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

solved: Cube.state == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

pin numbering

upper
0 1
2 3
'''

from itertools import combinations

def y_move_clocks(pins, direction):
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
    res = set(res)
    return res

def n_move_clocks(pins, direction):
    res = set(range(14)) - y_move_clocks(pins, direction)
    return res

def move(state, pins, direction, twist):
    move_clocks = y_move_clocks(pins, direction)
    res = [i for i in state]
    for i in move_clocks:
        res[i] += twist
        res[i] %= 12
    return res

solution = []

def search(depth, state, banned_pins):
    global solution
    if depth == 0:
        return set(state) == {0}
    for direction in range(2): # 0: lower, 1: upper
        pin_candidate = range(1, 5) if direction else range(4)
        for num_of_pins in pin_candidate: # pins that are pulled
            for pins_up in combinations(range(4), num_of_pins):
                pins = [True if i in pins_up else False for i in range(4)]
                if pins in banned_pins[direction]:
                    continue
                move_clocks_time = [state[i] for i in y_move_clocks(pins, direction)]
                not_move_clocks = n_move_clocks(pins, direction)
                if direction:
                    not_move_clocks -= set([9, 10, 11, 12, 13])
                else:
                    not_move_clocks -= set([1, 3, 4, 5, 7])
                time_candidate = [state[i] for i in not_move_clocks]
                twist_candidate = set([(i - j) % 12 for i in time_candidate for j in move_clocks_time])
                for twist in twist_candidate:
                    if twist == 0:
                        continue
                    n_state = move(state, pins, direction, twist)
                    n_banned_pins = [[i for i in j] for j in banned_pins]
                    n_banned_pins[direction].append(pins)
                    solution.append([pins, direction, twist])
                    if search(depth - 1, n_state, n_banned_pins):
                        return True
                    solution.pop()
                    #n_banned_pins[direction].pop()
    return False

def solver(state):
    global solution
    for depth in range(13):
        solution = []
        if search(depth, state, [[], []]):
            return solution
        print(depth)
    return -1

#test_cube = [3, 6, 0, 3, 6, 3, 0, 0, 0, 9, 9, 9, 0, 0]
test_cube = [5, 9, 6, 7, 9, 2, 8, 5, 1, 6, 9, 6, 0, 0] # UR1- DR2- DL5- UL0+ U5+ R5+ D5- L0+ ALL0+ y2 U6+ R3+ D0+ L6+ ALL3+
print(test_cube)

print(solver(test_cube))


