import cv2
import numpy as np
from security_system.constants import *
from security_system.masks import *
from security_system.utils import *

kernel = np.ones((5, 5), np.uint8)


def security_system(frame: cv2.typing.MatLike, security_pattern: List[str]) -> Tuple[cv2.typing.MatLike, List[str]]:
    detected_shapes = []

    # Flip so that the camera mirrors real video
    blurred = cv2.GaussianBlur(frame, (11, 11), 1)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Apply masks
    red_mask = cv2.inRange(hsv, RED_MASK_LOW[0], RED_MASK_LOW[1]) + \
        cv2.inRange(hsv, RED_MASK_HIGH[0], RED_MASK_HIGH[1])

    green_mask = cv2.inRange(
        hsv, GREEN_MASK[0], GREEN_MASK[1])

    blue_mask = cv2.inRange(hsv, BLUE_MASK[0], BLUE_MASK[1])

    purple_mask = cv2.inRange(
        hsv, PURPLE_MASK[0], PURPLE_MASK[1])

    # Identification
    masks = [
        (red_mask, TRIANGLE, "Red", (0, 0, 255)),
        (green_mask, SQUARE, "Green", (0, 255, 0)),
        (purple_mask, PENTAGON, "Purple", (255, 0, 255)),
        (blue_mask, HEXAGON, "Blue", (255, 0, 0))
    ]

    for mask, shape, color, draw_color in masks:
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours = get_contours(mask)

        detected_shapes.extend(detect_shapes(
            frame, contours, shape, color, draw_color))

    if len(detected_shapes) != 1:
        return (frame, security_pattern)

    shape = detected_shapes[0]

    if shape[0] == security_pattern[0]:
        print(shape)
        security_pattern.pop(0)

    return (frame, security_pattern)
