# coding:utf-8

import cv2
from math import sin, cos, pi
from statistics import variance
import numpy as np

def detector(direction):
    capture = cv2.VideoCapture(0)
    clocks = [-1 for _ in range(9)]
    #while(True):
    ret, frame = capture.read()
    size_x = 320 #240
    size_y = 240 #180
    #center_x = size_x // 2
    #center_y = size_y == 2
    frame = cv2.resize(frame, (size_x, size_y))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=30, minRadius=size_y // 16, maxRadius=size_y // 6)
    circles = [list(i) for i in np.uint16(np.around(circles))[0]]
    circles.sort(key=lambda x:(x[1] // (size_y // 10), x[0]))
    print(circles)
    if len(circles) < 9:
        print('error too few circles')
        return
    #dis = 52
    #radius = 20
    delta = [-1, 0, 1]
    for dy in range(3):
        for dx in range(3):
            if direction == 0 and not dy * 3 + dx in {1, 3, 4, 5, 7}:
                continue
            x, y, radius = circles[dy * 3 + dx]
            radius -= 1
            #x = center_x + delta[dx] * dis
            #y = center_y + delta[dy] * dis
            #cv2.circle(gray, (x, y), radius, (0, 0, 0), thickness=3, lineType=cv2.LINE_8, shift=0)
            value = [0 for _ in range(12)]
            for tim in range(12):
                deg = 30 * tim
                for r in range(radius // 2, radius * 2 // 3):
                    x_circle = int(x + r * sin(deg * pi / 180))
                    y_circle = int(y - r * cos(deg * pi / 180))
                    value[tim] += gray[y_circle, x_circle]
                
                for r in range(radius // 2, radius * 2 // 3):
                    x_circle = int(x + r * sin(deg * pi / 180))
                    y_circle = int(y - r * cos(deg * pi / 180))
                    cv2.circle(gray, (x_circle, y_circle), 1, (255, 255, 255), thickness=1, lineType=cv2.LINE_8, shift=0)
                
                value[tim] //= radius // 3
            min_value_idx = value.index(min(value))
            max_value_idx = value.index(max(value))
            arr_out_min = [i for i in value]
            del arr_out_min[min_value_idx]
            arr_out_max = [i for i in value]
            del arr_out_max[max_value_idx]
            coord = dy * 3 + dx
            if variance(arr_out_max) < variance(arr_out_min):
                clocks[coord] = max_value_idx
                x_circle = int(x + r * sin(max_value_idx * 30 * pi / 180))
                y_circle = int(y - r * cos(max_value_idx * 30 * pi / 180))
                cv2.circle(gray, (x_circle, y_circle), 3, (0, 0, 0), thickness=3, lineType=cv2.LINE_8, shift=0)
            else:
                clocks[coord] = min_value_idx
                x_circle = int(x + r * sin(min_value_idx * 30 * pi / 180))
                y_circle = int(y - r * cos(min_value_idx * 30 * pi / 180))
                cv2.circle(gray, (x_circle, y_circle), 3, (0, 0, 0), thickness=3, lineType=cv2.LINE_8, shift=0)
            #cv2.circle(gray, (x, y), (dy * 3 + dx + 2) * 3, (0, 0, 0), thickness=3, lineType=cv2.LINE_8, shift=0)
        #print(clocks)
        cv2.imwrite('test.png', gray)
        #cv2.imshow('title',gray)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
    capture.release()
    #cv2.destroyAllWindows()
    if direction == 0:
        return [clocks[i] for i in [1, 3, 4, 5, 7]]
    else:
        return clocks

print('detector initialized')

#print(detector(1))