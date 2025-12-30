import cv2
from security_system.security import security_system
from security_system.constants import *

SECURITY_PATTERN = [SQUARE, TRIANGLE, HEXAGON, PENTAGON]


cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    frame = security_system(frame, SECURITY_PATTERN)

    cv2.imshow("window", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
