from time import time, sleep
import serial
import RPi.GPIO as GPIO

def send_command(num, arg1, arg2=None, arg3=None):
    com = ''
    if arg2 != None:
        com += str(arg1) + ' ' + str(arg2) + ' '
        for i in arg3:
            com += str(i) + ' '
    else:
        for i in arg1:
            com += str(i) + ' '
    ser_motor[num].write((com + '\n').encode())

def controller(solution, rpm, slp_tim):
    strt_solv = time()
    for pins, direction, twist in solution:
        if GPIO.input(21) == GPIO.LOW:
            if bluetoothmode:
                client_socket.send('emergency\n')
            solvingtimevar.set('emergency stop')
            print('emergency stop')
            return -1
        send_command(0, pins)
        move_motors = [int(int(i) == direction) for i in pins]
        twist_fixed = twist * 30
        if twist_fixed > 180:
            twist_fixed = 180 - twist_fixed
        send_command(1, twist_fixed, rpm, move_motors)
        slptim = 2 * 60 / rpm * abs(twist_fixed) * 30 / 360
        sleep(slptim)
    solv_time = str(int((time() - strt_solv) * 1000) / 1000).ljust(5, '0')
    return solv_time


ser_motor = [None, None]
ser_motor[0] = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.01, write_timeout=0)
ser_motor[1] = serial.Serial('/dev/ttyUSB1', 115200, timeout=0.01, write_timeout=0)