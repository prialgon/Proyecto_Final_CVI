import cv2
from security_system.security import SecuritySystem
from security_system.constants import *
from pong.constants import *
from pong.threaded_camera import ThreadedCamera
from transition import TransitionSystem
import time
from fps import FPS
from pong.ball import Ball
from player_selection import PlayerSelector
from pong.game import PongGame1P, PongGame2P
from pong.tracker import AutoTracker

# Video Capture
cap = ThreadedCamera(0, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
time.sleep(1.0)

# Security system
security_system = SecuritySystem(
    security_pattern=[SQUARE, TRIANGLE, HEXAGON, PENTAGON])

# Transition
transition_system = TransitionSystem(duration=2)

# FPS
fps = FPS(max_fps=30, historic_frames=50)

# Pong
selector = PlayerSelector(3)
ball = Ball([WINDOW_WIDTH//2, WINDOW_HEIGHT//2], [14, -14], radius=10)
kcf_auto = AutoTracker(0, 380, 0, 720, "left")
pong_game = None

last_time = time.time()

while True:
    # ----- Delta Time -----
    current_time = time.time()
    deltatime = current_time - last_time
    last_time = current_time

    # ----- Read Frame -----
    success, frame = cap.read()

    if not success or frame is None:
        break

    frame = cv2.flip(frame, 1)

    # ----- States -----
    if security_system.finished:  # SET TO NOT WHEN WE WANT TO ACTIVATE
        frame = security_system.update(frame)
    elif transition_system.finished:  # SET TO NOT WHEN WE WANT TO ACTIVATE
        frame = transition_system.update(frame, deltatime)
    else:
        if not pong_game:
            if not selector.finished:
                selector.update(frame)
                frame = selector.draw(frame)
            else:
                if selector.gamemode == 1:
                    # 1 Player
                    pong_game = PongGame1P(ball, kcf_auto)
                elif selector.gamemode == 2:
                    # 2 Players
                    pong_game = PongGame2P(ball, kcf_auto)
                else:
                    raise ValueError(f"Invalid gamemode {selector.gamemode}.")

    # ----- FPS Updates -----
    deltatime = fps.limit(deltatime)
    frame = fps.update(frame, deltatime)

    if pong_game:
        frame = pong_game.update(frame, deltatime)

    # ----- Show Frame -----
    cv2.imshow("window", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
