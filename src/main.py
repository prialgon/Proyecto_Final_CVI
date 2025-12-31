import cv2
from security_system.security import security_system
from security_system.constants import *

initital_security_pattern = [SQUARE, TRIANGLE, HEXAGON, PENTAGON]

security_pattern = initital_security_pattern.copy()

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

shape_consequent_counter = 0

while True:
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    if len(security_pattern) > 0:
        frame, security_pattern, shape_consequent_counter = security_system(
            frame, security_pattern, shape_consequent_counter)

    cv2.imshow("window", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
