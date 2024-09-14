import cv2
import mediapipe as mp
import os
from Hand_tracking_module import HandTracking
import numpy as np
import time  # Import time module to calculate FPS

# List images for painting
img_path = os.listdir("hand tracking projects/opencv/images for painting")
img_list = []
for i in img_path:
    img = cv2.imread(r"hand tracking projects/opencv/images for painting/{}".format(i))
    resize_frame = cv2.resize(img, (1280, 150))
    img_list.append(resize_frame)

# Capture webcam
vid = cv2.VideoCapture(0)

hd = HandTracking()
vid.set(3, 1280)
vid.set(4, 720)
wcam = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
hcam = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
draw_color = (0, 0, 0)
img_canvas = np.zeros((720, 1280, 3), np.uint8)
xp, yp = 0, 0

# Initialize variables for calculating FPS
prev_time = 0

while True:
    ret, frame = vid.read()
    frame = cv2.flip(frame, 1)
    if not ret:
        break

    # Find hands and position
    frame = hd.find_hands(frame)
    frame, position = hd.find_position(frame, False, [3, 4, 6, 8, 10, 12, 14, 16, 18, 20])

    finger = []
    if position:
        if position[0][0] >= position[1][0]:
            finger.append(1)
        else:
            finger.append(0)

        tip = [3, 5, 7, 9]
        base = [2, 4, 6, 8]
        for i in range(4):
            if position[tip[i]][1] < position[base[i]][1]:
                finger.append(1)
            else:
                finger.append(0)

        x1, y1 = position[3][0], position[3][1]
        x2, y2 = position[5][0], position[5][1]
        x, y = int((x1 + x2) // 2), int((y1 + y2) // 2)

        # Selection Mode
        if finger[1] == 1 and finger[2] == 1 and finger[0] != 1 and finger[3] != 1 and finger[4] != 1:
            cv2.circle(frame, (x1, y1), 5, (255, 0, 0), -1)
            cv2.circle(frame, (x2, y2), 5, (255, 0, 0), -1)

            if y1 < 125:
                if x1 > 0 and x1 < 400:
                    frame[0:150, 0:1280] = img_list[1]
                    draw_color = (255, 0, 0)
                elif x1 > 400 and x1 < 700:
                    frame[0:150, 0:1280] = img_list[2]
                    draw_color = (0, 255, 0)
                elif x1 > 700 and x1 < 1000:
                    frame[0:150, 0:1280] = img_list[3]
                    draw_color = (0, 0, 255)
                else:
                    frame[0:150, 0:1280] = img_list[0]
                    draw_color = (0, 0, 0)
            cv2.circle(frame, (x, y), 25, draw_color, -1)

        # Drawing Mode
        if finger[1] == 1 and finger[2] != 1 and finger[0] != 1 and finger[3] != 1 and finger[4] != 1:
            cv2.circle(frame, (x1, y1), 5, (255, 0, 0), -1)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            if draw_color == (0, 0, 0):
                cv2.line(frame, (xp, yp), (x1, y1), draw_color, 50)
                cv2.line(img_canvas, (xp, yp), (x1, y1), draw_color, 50)
            else:
                cv2.line(frame, (xp, yp), (x1, y1), draw_color, 5)
                cv2.line(img_canvas, (xp, yp), (x1, y1), draw_color, 5)
        xp, yp = x1, y1

    # Combine canvas and frame
    gray_canva = cv2.cvtColor(img_canvas, cv2.COLOR_BGR2GRAY)
    _, thresh_frame = cv2.threshold(gray_canva, 50, 255, cv2.THRESH_BINARY_INV)
    thresh_frame = cv2.cvtColor(thresh_frame, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, thresh_frame)
    frame = cv2.bitwise_or(frame, img_canvas)

    # Calculate FPS
    current_time = time.time()
    fps = 1 / max((current_time - prev_time), 1e-6)  # Avoid division by zero
    prev_time = current_time

    # Display FPS on the frame
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Virtual Painter', frame)
    cv2.imshow('Canvas', img_canvas)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
