import cv2
from numpy import ndarray
from constants import *
from utils import get_roi_points
from typing import Tuple


def create_tracker(frame: cv2.typing.MatLike, low_x: int, high_x: int, low_y: int, high_y: int) -> cv2.legacy.TrackerKCF:
    kcf = cv2.legacy.TrackerKCF_create()

    masked = frame[low_x:high_x, low_y:high_y]

    kcf.init(masked, TRACK_WINDOW)

    return kcf


def update_kcf(kcf: cv2.legacy.TrackerKCF, frame: cv2.typing.MatLike, low_x: int, high_x: int, low_y: int, high_y: int) -> Tuple[bool, cv2.typing.Rect2d]:
    masked = frame[low_x:high_x, low_y:high_y]
    detected, roi = kcf.update(masked)

    return detected, roi


def draw_box(frame: cv2.typing.MatLike, roi: cv2.typing.Rect2d, thickness: int = -1, color: int = 255) -> cv2.typing.MatLike:
    rectframe = frame.copy()
    p1, p2 = get_roi_points(roi)
    rectframe = cv2.rectangle(rectframe, p1, p2, color, thickness)
    return rectframe
