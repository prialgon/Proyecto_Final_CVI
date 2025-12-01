import cv2
import numpy as np


def auto_mask(img_bgr, h_tol=10, s_tol=40, v_tol=40):
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    pixels = hsv.reshape((-1, 3))

    # --- 0. Remove white / grey / very bright pixels ---
    # White = low S, high V
    not_white = (pixels[:, 1] > 40) & (pixels[:, 2] < 220)
    filtered = pixels[not_white]

    # If filtering removes everything, fall back to all pixels
    if len(filtered) == 0:
        filtered = pixels

    # --- 1. Compute dominant remaining HSV ---
    h, s, v = np.median(filtered, axis=0).astype(int)

    # --- 2. Build mask ranges ---
    lower = np.array([
        max(h - h_tol, 0),
        max(s - s_tol, 0),
        max(v - v_tol, 0)
    ])

    upper = np.array([
        min(h + h_tol, 179),
        min(s + s_tol, 255),
        min(v + v_tol, 255)
    ])

    # --- 3. Create mask ---
    mask = cv2.inRange(hsv, lower, upper)

    return lower, upper, mask


img = cv2.imread("data/orange.jpg")

lower, upper, mask = auto_mask(img)

print("Lower HSV:", lower)
print("Upper HSV:", upper)

cv2.imshow("Mask", mask)
cv2.waitKey(0)
