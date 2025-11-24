import cv2
import os
import glob
from auxiliary import *


WORKDIR = os.getcwd()
# patterns_path = "data/security_system_patterns/*.png"


# path = os.path.join(WORKDIR, patterns_path)

# gb_path = glob.glob(path)

# imgs = load_images(gb_path)

i = 4

# img = imgs[i]

width = 1280
height = 720
camera_index = 0

cap = cv2.VideoCapture(camera_index)
if not cap.isOpened():
    print(f"Could not open the camera (index {camera_index}).")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

window_name = "Live Camera - press 'q' to quit"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # resizable window

_, frame_before = cap.read()

# Mask
lower_red1 = np.array([0, 150, 150])
upper_red1 = np.array([10, 255, 255])

lower_red2 = np.array([170, 150, 150])
upper_red2 = np.array([180, 255, 255])

# --- Vibrant BLUE ---
lower_blue = np.array([95, 150, 150])
upper_blue = np.array([130, 255, 255])

# --- Vibrant GREEN ---
lower_green = np.array([40, 150, 150])
upper_green = np.array([85, 255, 255])

# --- Vibrant ORANGE ---
lower_orange = np.array([10, 150, 150])
upper_orange = np.array([25, 255, 255])


while True:
    ret, frame = cap.read()

    # frame = 255 - cv2.absdiff(clean_frame, frame_before)

    frame = cv2.flip(frame, 1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)

    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    red_frame = cv2.bitwise_and(frame, frame, mask=red_mask)
    blue_frame = cv2.bitwise_and(frame, frame, mask=blue_mask)
    green_frame = cv2.bitwise_and(frame, frame, mask=green_mask)
    orange_frame = cv2.bitwise_and(frame, frame, mask=orange_mask)

    frame = green_frame

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5),
                            cv2.BORDER_DEFAULT)
    # ret, thresh = cv2.threshold(blur, 200, 255,
    #                             cv2.THRESH_BINARY_INV)

    edges = cv2.Canny(gray, 1, 1)

    contours, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) < 500:
            continue

        epsilon = 0.02 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        cv2.drawContours(frame, [approx], -1, (255, 255, 255), 2)

        if len(approx) > 10:
            break

        for point in approx:
            x, y = point.ravel()
            cv2.circle(frame, (x, y), 6, (255, 255, 255), -1)

    cv2.imshow(window_name, frame)

    # frame_before = clean_frame
