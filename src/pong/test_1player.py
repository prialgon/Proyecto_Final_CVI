import time
import cv2
from ball import Ball
from constants import *
from tracker import Tracker
from fps import FPS
from text_manager import add_text

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)

window_name = "Live Camera - press 'q' to quit"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

ball = Ball([10, 700], [14, -14], radius=10)
fps = FPS(frames=50)

trained_right = False
trained_left = False
trained = False

kcf_right = None
kcf_left = None

recalibrate_timer = 5

time.time()
while True:
    start_time = time.time()

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # bwframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q') or key == 27:
        break
    elif recalibrate_timer < 0 and recalibrate_timer != -100:
        kcf_right = Tracker(frame, 900, 1280, 0, 720, "right")
        trained = True

    if trained:
        if kcf_right is None:
            raise ValueError()

        
        kcf_right.update(frame, 900, 1280, 0, 720)

        # if kcf_right.detected:
            
        frame = kcf_right.draw_box(frame)
        ball.update_paddle_collisions(kcf_right.roi)

        if not kcf_right.detected:
            recalibrate_timer = 5 if recalibrate_timer < 0 else recalibrate_timer
            frame = add_text(
                frame, f"Recalibrating in {int(recalibrate_timer)}...", "top")
            frame = cv2.rectangle(frame, (1000, 200), (1280, 480),
                                  color=(0, 0, 255), thickness=2)
        else:
            recalibrate_timer = -100


    else:
        frame = add_text(frame, f"Place your hand in the red square", "top")
        frame = add_text(frame, f"{int(recalibrate_timer)}", "center", 5)
        frame = cv2.rectangle(frame, (1000, 200), (1280, 480),
                              color=(0, 0, 255), thickness=2)

    if trained:
        ball.update_position()

        frame = ball.draw(frame)

    end_time = time.time()

    deltatime = end_time - start_time

    if recalibrate_timer > 0:
        recalibrate_timer -= deltatime

    frame = fps.update(frame, deltatime)
    
    cv2.imshow(window_name, frame)

cap.release()
cv2.destroyAllWindows()
