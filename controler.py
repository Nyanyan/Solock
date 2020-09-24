from time import time

# アクチュエータを動かすコマンドを送る
# Send commands to move actuators
def move_actuator(num, arg1, arg2, arg3=None):
    if arg3 == None:
        com = str(arg1) + ' ' + str(arg2)
    else:
        com = str(arg1) + ' ' + str(arg2) + ' ' + str(arg3)
    ser_motor[num].write((com + '\n').encode())

def controller(solution, rpm, slp_tim):
    strt_solv = time()
    for 
        
        if GPIO.input(21) == GPIO.LOW:
            if bluetoothmode:
                client_socket.send('emergency\n')
            solvingtimevar.set('emergency stop')
            print('emergency stop 1')
            return
        
        if i != 0:
            grab = ans[i][0] % 2
            for j in range(2):
                move_actuator(j, grab, 1000)
            sleep(slp1)
            for j in range(2):
                move_actuator(j, (grab + 1) % 2, 2000)
            sleep(slp2)
        ser_num = ans[i][0] // 2
        offset = 0
        before = ser_motor[ans[i][0] // 2].in_waiting
        move_actuator(ser_num, ans[i][0] % 2, ans[i][1] * 90 + offset, rpm)
        max_turn = abs(ans[i][1])
        flag = i < len(ans) - 1 and ans[i + 1][0] % 2 == ans[i][0] % 2
        if flag:
            before2 = ser_motor[ans[i + 1][0] // 2].in_waiting
            move_actuator(ans[i + 1][0] // 2, ans[i + 1][0] % 2, ans[i + 1][1] * 90 + offset, rpm)
            max_turn = max(max_turn, abs(ans[i + 1][1]))
            '''
            while not before2 - ser_motor[ans[i + 1][0] // 2].in_waiting:
                if GPIO.input(21) == GPIO.LOW:
                    ser_motor[ans[i + 1][0] // 2].write(b's\n')
                    ser_motor[ans[i + 1][0] // 2].flush()
                    ser_motor[ans[i][0] // 2].write(b's\n')
                    ser_motor[ans[i][0] // 2].flush()
                    solvingtimevar.set('emergency stop')
                    print('emergency stop 2')
                    return
            
        while not before - ser_motor[ans[i][0] // 2].in_waiting:
            if GPIO.input(21) == GPIO.LOW:
                ser_motor[ans[i][0] // 2].write(b's\n')
                ser_motor[ans[i][0] // 2].flush()
                solvingtimevar.set('emergency stop')
                print('emergency stop 2')
                return
        #sleep(slp3)
        '''
        
        slptim = 2 * 60 / rpm * (max_turn * 90 - offset) / 360 * ratio
        sleep(slptim)
        
        '''
        move_actuator(ser_num, ans[i][0] % 2, -offset, rpm)
        if flag:
            move_actuator(ans[i + 1][0] // 2, ans[i + 1][0] % 2, -offset, rpm)
        #slptim = 2 * 60 / rpm * (-offset) / 360 * 0.9
        #sleep(slptim)
        '''
        i += 1 + int(flag)
        #slptim2 = abs(2 * 60 / rpm * offset / 360)
        #sleep(slptim2)
    solv_time = str(int((time() - strt_solv) * 1000) / 1000).ljust(5, '0')
    if bluetoothmode:
        client_socket.send(solv_time + '\n')
    solvingtimevar.set(solv_time + 's')
    print('solving time:', solv_time, 's')


ser_motor = [None, None]
ser_motor[0] = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.01, write_timeout=0)
ser_motor[1] = serial.Serial('/dev/ttyUSB1', 115200, timeout=0.01, write_timeout=0)