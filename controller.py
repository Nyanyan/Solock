# coding:utf-8

from time import time, sleep
import serial

def send_command(num, arg1, arg2=None, arg3=None):
    com = ''
    if num:
        com += str(arg1) + ' ' + str(arg2) + ' '
        for i in arg3:
            com += str(int(i)) + ' '
    else:
        for i in arg1:
            com += str(int(i)) + ' '
    ser_motor[num].write((com + '\n').encode())

def controller(solution, rpm, slp_tim, ratio):
    strt_solv = time()
    idx = 0
    len_solution = len(solution)
    while idx < len_solution:
        pins, direction, twist = solution[idx]
        #print(pins, direction, twist)
        send_command(0, pins)
        sleep(slp_tim)
        move_motors = [int(i) == direction for i in pins]
        twist_fixed = twist * 30
        if twist_fixed > 180:
            twist_fixed = twist_fixed - 360
        send_command(1, twist_fixed, rpm, move_motors)
        max_twist = abs(twist_fixed)
        if idx + 1 < len_solution and solution[idx + 1][0] == pins:
            n_pins, n_direction, n_twist = solution[idx + 1]
            n_move_motors = [int(i) == n_direction for i in n_pins]
            n_twist_fixed = n_twist * 30
            if n_twist_fixed > 180:
                n_twist_fixed = n_twist_fixed - 360
            send_command(1, n_twist_fixed, rpm, n_move_motors)
            max_twist = max(max_twist, abs(n_twist_fixed))
            idx += 1
        slp_tim_motor = 2 * 60 / rpm * max_twist / 360 * ratio
        sleep(slp_tim_motor)
        idx += 1
    solv_time = str(int((time() - strt_solv) * 1000) / 1000).ljust(5, '0')
    return solv_time

ser_motor = [None, None]
ser_motor[0] = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.01, write_timeout=0)
ser_motor[1] = serial.Serial('/dev/ttyUSB1', 115200, timeout=0.01, write_timeout=0)

print('controller initialized')