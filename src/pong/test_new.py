import time
import cv2
from ball import Ball
from constants import *
from tracking import *
from utils import *

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)

window_name = "Live Camera - press 'q' to quit"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

ball = Ball([10, 700], [14, -14])

trained = False

time.time()
while True:
    start_time = time.time()

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q') or key == 27:
        break
    elif key == ord('s'):
        kcf = create_tracker(frame, 0, 720, 900, 1280)
        trained = True

    if trained:
        detected, roi = update_kcf(kcf, frame, 0, 720, 900, 1280)
        if detected:
            frame = draw_box(frame, roi)
            if ball.check_collision(roi):
                ball.update_collision(roi)
    else:
        frame = cv2.rectangle(frame, (1000, 200), (1280, 480),
                              color=(0, 0, 255), thickness=2)

    frame = ball.draw(frame)

    ball.check_bounding_box_collision()

    ball.update_position()

    end_time = time.time()

    deltatime = end_time - start_time

    frame = show_fps(frame, deltatime)

    cv2.imshow(window_name, frame)

cap.release()
cv2.destroyAllWindows()
