# coding:utf-8

from time import time, sleep
import serial
import RPi.GPIO as GPIO

def send_command_pins(pins):
    com = ''
    for i in pins:
        com += str(int(i)) + ' '
    ser_motor[0].write((com + '\n').encode())

def send_command_motors(rpm, twist1, twist2, move_motors):
    com = str(rpm) + ' ' + str(twist1) + ' ' + str(twist2) + ' '
    for i in move_motors:
        com += str(int(i)) + ' '
    ser_motor[1].write((com + '\n').encode())

def controller(solution, rpm, slp_tim, ratio):
    strt_solv = time()
    idx = 0
    len_solution = len(solution)
    GPIO.output(4,GPIO.HIGH)
    sleep(0.005)
    GPIO.output(4,GPIO.LOW)
    while idx < len_solution:
        pins, direction, twist = solution[idx]
        #print(pins, direction, twist)
        send_command_pins(pins)
        sleep(slp_tim)
        move_motors = [int(i) == direction for i in pins]
        twist_fixed = twist * 30
        if twist_fixed > 180:
            twist_fixed = twist_fixed - 360
        twist1 = twist_fixed
        twist2 = 0
        max_twist = abs(twist_fixed)
        if idx + 1 < len_solution and solution[idx + 1][0] == pins:
            _, _, n_twist = solution[idx + 1]
            n_twist_fixed = n_twist * 30
            if n_twist_fixed > 180:
                n_twist_fixed = n_twist_fixed - 360
            twist2 = n_twist_fixed
            max_twist = max(max_twist, abs(n_twist_fixed))
            idx += 1
        #print(twist1, twist2)
        #print([int(i) for i in move_motors])
        send_command_motors(rpm, twist1, twist2, move_motors)
        #slp_tim_motor = 2 * 60 / rpm * max_twist / 360 * ratio
        #sleep(slp_tim_motor)
        s = b''
        while s == b'':
            s = ser_motor[1].read(3)
            #print('a', s, 'a')
        idx += 1
    GPIO.output(4,GPIO.HIGH)
    sleep(0.005)
    GPIO.output(4,GPIO.LOW)
    solv_time = 'info' #str(int((time() - strt_solv) * 1000) / 1000).ljust(5, '0')
    return solv_time

ser_motor = [None, None]
ser_motor[0] = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.01)
ser_motor[1] = serial.Serial('/dev/ttyUSB1', 115200, timeout=0.01)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.output(4,GPIO.LOW)

print('controller initialized')