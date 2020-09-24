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

def move(state, pins, direction, twist):
    move_clocks = []
    if direction: # move upper clocks
        clock_candidate = [[0, 1, 3, 4], [1, 2, 4, 5], [3, 4, 6, 7], [4, 5, 7, 8]]
        for i, j in enumerate(pins):
            if j:
                move_clocks.extend(clock_candidate[i])
    else: # move lower clocks
        clock_candidate = [[0, 9, 12, 11], [9, 2, 11, 10], [12, 11, 6, 13], [11, 10, 13, 8]]
        for i, j in enumerate(pins):
            if not j:
                move_clocks.extend(clock_candidate[i])
    move_clocks = set(move_clocks)
    res = [i for i in state]
    for i in move_clocks:
        res[i] += twist
        res[i] %= 12
    return res

scrambled_cube = [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0] # UR1+
solution = []

def search(state, banned_twist):
    global solution
    

def solver(state):
    global solution
    solution = []
    search(state, [])
    return solution





