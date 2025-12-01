import cv2
import os
import glob
from auxiliary import *
import time


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
lower_red1 = np.array([0, 120, 40])
upper_red1 = np.array([10, 255, 150])

lower_red2 = np.array([170, 120, 40])
upper_red2 = np.array([255, 255, 150])

lower_red = np.array([0, 120, 120])
upper_red = np.array([10, 255, 255])


# --- BLUE (vibrant + darker) ---
lower_blue = np.array([110, 100, 80])
upper_blue = np.array([130, 255, 255])

lower_blue = np.array([105, 80, 40])
upper_blue = np.array([130, 255, 120])

lower_blue = np.array([108, 60, 60])
upper_blue = np.array([118, 150, 140])


# --- GREEN (vibrant + darker) ---
lower_green = np.array([40, 100, 80])
upper_green = np.array([85, 255, 255])

lower_green = np.array([35, 80, 40])
upper_green = np.array([85, 255, 120])

lower_green = np.array([35, 40, 60])
upper_green = np.array([45, 150, 200])


# --- ORANGE (vibrant + darker) ---
lower_orange = np.array([10, 150, 120])
upper_orange = np.array([25, 255, 255])

lower_orange = np.array([10, 100, 40])
upper_orange = np.array([25, 255, 120])


# GOOD ONES
lower_red = np.array([0, 100, 120])
upper_red = np.array([10, 255, 255])


lower_green = np.array([30, 40, 100])
upper_green = np.array([49, 150, 255])

lower_blue = np.array([103,  77, 50])
upper_blue = np.array([123, 157, 255])

lower_orange = np.array([4,  117, 187])
upper_orange = np.array([24, 197, 255])

lasttime = time.perf_counter()
while True:
    actual = time.perf_counter()

    deltatime = actual - lasttime

    lasttime = actual

    ret, frame = cap.read()

    # frame = 255 - cv2.absdiff(clean_frame, frame_before)

    frame = cv2.flip(frame, 1)

    orig_frame = frame.copy()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    # Y, Cr, Cb = cv2.split(ycrcb)
    # skin_mask = cv2.inRange(ycrcb, np.array(
    #     [0, 135, 85]), np.array([255, 180, 135]))
    # red_mask = cv2.inRange(hsv, lower_red, upper_red)
    # red_mask = cv2.bitwise_and(red_mask, cv2.bitwise_not(skin_mask))

    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)

    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    # red_mask = cv2.bitwise_xor(red_mask1, red_mask2)

    red_frame = cv2.bitwise_and(frame, frame, mask=red_mask)
    blue_frame = cv2.bitwise_and(frame, frame, mask=blue_mask)
    green_frame = cv2.bitwise_and(frame, frame, mask=green_mask)
    orange_frame = cv2.bitwise_and(frame, frame, mask=orange_mask)

    frame = red_frame

    frames = [red_frame, blue_frame, green_frame, orange_frame]

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5),
                            cv2.BORDER_DEFAULT)

    edges = cv2.Canny(gray, 1, 1)

    contours, _ = cv2.findContours(
        edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) < 400:
            continue

        epsilon = 0.02 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # cv2.drawContours(frame, [approx], -1, (255, 255, 255), 2)

        print(len(approx))

        # Star: 10
        # Triangle: 3/4
        # Rectangle: 4
        # Hexagon:6

        if len(approx) != 3:
            break

        # for point in approx:
        #     x, y = point.ravel()
        #     cv2.circle(frame, (x, y), 6, (255, 255, 255), -1)

        M = cv2.moments(cnt)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 7, (0, 0, 255), -1)

    cv2.putText(frame, f'{int(1/(deltatime))} FPS', (0, 20), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow(window_name, frame)

    # frame_before = clean_frame
