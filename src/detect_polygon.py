import cv2
import os
import glob
from auxiliary import *


WORKDIR = os.getcwd()
patterns_path = "data/security_system_patterns/*.png"


path = os.path.join(WORKDIR, patterns_path)

gb_path = glob.glob(path)

imgs = load_images(gb_path)

i = 4

img = imgs[i]

gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

gray = cv2.GaussianBlur(gray, (5, 5), 1.4)

edges = cv2.Canny(gray, 50, 150)

contours, _ = cv2.findContours(
    edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    if cv2.contourArea(cnt) < 200:
        continue

    epsilon = 0.02 * cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)

    cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)

    for point in approx:
        x, y = point.ravel()
        cv2.circle(img, (x, y), 6, (0, 255, 0), -1)

show_image(edges)
show_image(img)
