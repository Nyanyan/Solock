import cv2
from math import sin, cos, pi

def detect(direction):
    capture = cv2.VideoCapture(0)

    while(True):
        ret, frame = capture.read()
        # resize the window
        size_x = 400
        size_y = 300
        center_x = size_x // 2
        center_y = size_y // 2
        frame = cv2.resize(frame, (size_x, size_y))
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        dis = 50
        radius = 20
        delta = [-1, 0, 1]
        for dy in range(3):
            for dx in range(3):
                x = center_x + delta[dx] * dis
                y = center_y + delta[dy] * dis
                cv2.circle(frame, (x, y), radius, (0, 0, 0), thickness=3, lineType=cv2.LINE_8, shift=0)
                colors = [None for _ in range(12)]
                for tim in range(12):
                    deg = 30 * tim
                    x_circle = int(x + radius // 4 * 3 * sin(deg * pi / 180))
                    y_circle = int(y + radius // 4 * 3 * cos(deg * pi / 180))
                    cv2.circle(frame, (x_circle, y_circle), 2, (0, 0, 0), thickness=3, lineType=cv2.LINE_8, shift=0)
                    colors[tim] = hsv[x_circle, y_circle][2]
                
                print(colors)





        cv2.imshow('title',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

detect(0)