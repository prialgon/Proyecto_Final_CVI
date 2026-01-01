import cv2
from typing import Tuple


def get_roi_points(roi: cv2.typing.Rect2d) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    pt1 = (int(roi[0]), int(roi[1]))
    pt2 = (int(roi[0] + roi[2]), int(roi[1] + roi[3]))
    return pt1, pt2
