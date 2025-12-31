import cv2
from numpy import ndarray
from pong.constants import *
from typing import Tuple


def create_tracker(frame: cv2.typing.MatLike, mask: ndarray) -> cv2.legacy.TrackerKCF:
    tracker = cv2.legacy.TrackerKCF()

    kcf = tracker.create()

    masked = frame[mask]

    kcf.init(masked, TRACK_WINDOW)

    return kcf


if detected:
    if (ball_position[0] > pt1[0]) and (ball_position[1] > pt1[1] and ball_position[1] < pt2[1]):

        if not changed_vec:
            if (ball_direction[0] - pt1[0] < ball_direction[1] - pt1[1]) or (ball_direction[0] - pt1[0] < ball_direction[1] - pt2[1]):
                ball_direction = rebound(ball_direction, "x")

            else:
                ball_direction = rebound(ball_direction, "y")
            changed_vec = True
        else:
            changed_vec = False
    final_frame = rectframe


def detect_object(kcf: cv2.legacy.TrackerKCF, frame: cv2.typing.MatLike, mask: ndarray) -> Tuple[bool, cv2.typing.Rect2d]:
    masked = frame[mask]
    detected, roi = kcf.update(masked)

    return detected, roi


def calculate_points(roi: cv2.typing.Rect2d) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    pt1 = (int(roi[0])+900, int(roi[1]))
    pt2 = (int(roi[0]+900 + roi[2]), int(roi[1] + roi[3]))
    return pt1, pt2


def draw_box(frame: cv2.typing.MatLike, roi: cv2.typing.Rect2d, thickness: int = -1, color: int = 255) -> cv2.typing.MatLike:
    rectframe = frame.copy()
    p1, p2 = calculate_points(roi)
    rectframe = cv2.rectangle(rectframe, p1, p2, color, thickness)
    return rectframe
