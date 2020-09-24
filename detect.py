import cv2
from math import sin, cos, pi
from statistics import variance

def detect(direction):
    capture = cv2.VideoCapture(0)
    clocks = [-1 for _ in range(9)]
    while(True):
        ret, frame = capture.read()
        # resize the window
        size_x = 400
        size_y = 300
        center_x = size_x // 2
        center_y = size_y // 2
        frame = cv2.resize(frame, (size_x, size_y))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dis = 70
        radius = 25
        delta = [-1, 0, 1]
        for dy in range(3):
            for dx in range(3):
                x = center_x + delta[dx] * dis
                y = center_y + delta[dy] * dis
                cv2.circle(gray, (x, y), radius, (0, 0, 0), thickness=3, lineType=cv2.LINE_8, shift=0)
                value = [0 for _ in range(12)]
                for tim in range(12):
                    deg = 30 * tim
                    for r in range(radius // 3, radius // 2):
                        x_circle = int(x + r * sin(deg * pi / 180))
                        y_circle = int(y - r * cos(deg * pi / 180))
                        cv2.circle(gray, (x_circle, y_circle), 1, (tim * 255 // 12, 0, 0), thickness=1, lineType=cv2.LINE_8, shift=0)
                        if dy == 0 and dx == 0:
                            print(gray[x_circle, y_circle], end=' ')
                        value[tim] += gray[x_circle, y_circle]
                    if dy == 0 and dx == 0:
                        print('')
                    value[tim] //= radius // 2 - radius // 3
                min_value_idx = value.index(min(value))
                max_value_idx = value.index(max(value))
                arr_out_min = [i for i in value]
                del arr_out_min[min_value_idx]
                arr_out_max = [i for i in value]
                del arr_out_max[max_value_idx]
                coord = dy * 3 + dx
                if variance(arr_out_max) < variance(arr_out_min):
                    clocks[coord] = max_value_idx
                else:
                    clocks[coord] = min_value_idx
                if dx == dy == 0:
                    print(variance(arr_out_max), variance(arr_out_min), value)
        print(clocks)





        cv2.imshow('title',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

detect(0)