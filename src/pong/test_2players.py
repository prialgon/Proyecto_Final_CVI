import time
import cv2
from ball import Ball
from constants import *
from tracker import Tracker
from fps import FPS

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)

window_name = "Live Camera - press 'q' to quit"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

ball = Ball([10, 700], [14, -14])
fps = FPS(frames=50)

trained_right = False
trained_left = False
trained = False

kcf_right = None
kcf_left = None

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
        if not trained_right:
            kcf_right = Tracker(frame, 900, 1280, 0, 720, "right")
            trained_right = True
        elif not trained_left:
            kcf_left = Tracker(frame, 0, 380, 0, 720, "left")
            trained_left = True

        if trained_right and trained_left:
            trained = True

    if trained:
        if kcf_right is None:
            raise ValueError()
        if kcf_left is None:
            raise ValueError()

        kcf_right.update(frame, 900, 1280, 0, 720)

        kcf_left.update(frame, 0, 380, 0, 720)

        if kcf_right.detected:
            print("HI")
            frame = kcf_right.draw_box(frame)
            print(kcf_right.roi)
            if ball.check_collision(kcf_right.roi):
                ball.update_collision(kcf_right.roi)

        if kcf_left.detected:
            # print(kcf_left.roi)
            frame = kcf_left.draw_box(frame)
            if ball.check_collision(kcf_left.roi):
                ball.update_collision(kcf_left.roi)
    else:
        if not trained_right:
            frame = cv2.rectangle(frame, (1000, 200), (1280, 480),
                                  color=(0, 0, 255), thickness=2)
        elif not trained_left:
            frame = cv2.rectangle(frame, (0, 200), (280, 480),
                                  color=(0, 0, 255), thickness=2)

    frame = ball.draw(frame)

    ball.check_bounding_box_collision()

    ball.update_position()

    end_time = time.time()

    deltatime = end_time - start_time

    frame = fps.update(frame, deltatime)

    cv2.imshow(window_name, frame)

cap.release()
cv2.destroyAllWindows()
