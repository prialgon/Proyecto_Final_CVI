import time
import cv2
from ball import Ball
from constants import *
from tracker import Tracker, AutoTracker
from fps import FPS
from text_manager import add_text
from threaded_camera import ThreadedCamera

cap = ThreadedCamera(0, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)

# Give the camera a moment to warm up
time.sleep(1.0)

window_name = "Live Camera - press 'q' to quit"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

ball = Ball([300, 700], [14, -14], radius=10)
fps = FPS(frames=50)

trained = False
kcf_right = None

recalibrate_timer = 5
score = 0
points = 0

kcf_auto = AutoTracker(0, 380, 0, 720, "left")

while True:
    start_time = time.time()

    # Instant read
    ret, frame = cap.read()

    # If the camera hasn't sent a frame yet, skip this loop iteration
    if not ret or frame is None:
        continue

    # 1. Flip immediately (Performance Tip: Do this after read)
    frame = cv2.flip(frame, 1)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break

    # --- RECALIBRATION LOGIC ---
    # Trigger logic only when timer hits 0, creating the tracker ONCE
    if not trained and recalibrate_timer < 0 and recalibrate_timer != -100:
        # Define ROI (Region of Interest) for the right hand
        kcf_right = Tracker(frame, 900, 1280, 0, 720, "right")
        trained = True
        recalibrate_timer = -100  # Stop timer logic

    if trained:
        if kcf_right is None:
            raise ValueError("Tracker lost")

        # Update tracker
        kcf_right.update(frame, 900, 1280, 0, 720)

        # Draw box
        frame = kcf_right.draw_box(frame)

        # Update Ball Physics
        ball.update_paddle_collisions(kcf_right.roi)

        # Lost Tracking Logic
        if not kcf_right.detected:
            # If we lose the hand, start counting down again
            trained = False
            recalibrate_timer = 5
            kcf_right = None  # Destroy tracker to save memory/processing

    else:
        # Not Trained / Recalibrating
        frame = add_text(frame, "Place your hand in the red square", "top")

        display_timer = int(
            recalibrate_timer) if recalibrate_timer > 0 else "GO!"
        frame = add_text(frame, f"{display_timer}", "center", 5)

        cv2.rectangle(frame, (1000, 200), (1280, 480),
                      color=(0, 0, 255), thickness=2)

    # --- AUTO PADDLE (Left) ---
    if trained:
        kcf_auto.update(ball.y)
        ball.update_paddle_collisions(kcf_auto.roi)
        points = ball.update_position()
        frame = ball.draw(frame)

    frame = kcf_auto.draw_box(frame)

    # --- FPS & TIMING ---
    end_time = time.time()
    deltatime = end_time - start_time

    if recalibrate_timer > 0:
        recalibrate_timer -= deltatime

    score += points
    frame = fps.update(frame, deltatime)
    frame = add_text(frame, f"Score: {score}", "right_corner")

    cv2.imshow(window_name, frame)

cap.release()
cv2.destroyAllWindows()
