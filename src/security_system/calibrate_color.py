import cv2
import numpy as np


def nothing(x) -> None:
    pass


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 640, 240)

# Default
cv2.createTrackbar("Hue Min", "Trackbars", 125, 179, nothing)
cv2.createTrackbar("Hue Max", "Trackbars", 160, 179, nothing)
cv2.createTrackbar("Sat Min", "Trackbars", 100, 255, nothing)
cv2.createTrackbar("Sat Max", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("Val Min", "Trackbars", 70, 255, nothing)
cv2.createTrackbar("Val Max", "Trackbars", 255, 255, nothing)

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("Hue Min", "Trackbars")
    h_max = cv2.getTrackbarPos("Hue Max", "Trackbars")
    s_min = cv2.getTrackbarPos("Sat Min", "Trackbars")
    s_max = cv2.getTrackbarPos("Sat Max", "Trackbars")
    v_min = cv2.getTrackbarPos("Val Min", "Trackbars")
    v_max = cv2.getTrackbarPos("Val Max", "Trackbars")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Show the mask (Black/White) to judge quality
    cv2.imshow("Mask (Tune this!)", mask)
    cv2.imshow("Original", result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print(f"Final Values: Lower={lower}, Upper={upper}")
        break

cap.release()
cv2.destroyAllWindows()
