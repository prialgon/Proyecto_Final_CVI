import cv2
from typing import Tuple, List


def get_roi_points(roi: cv2.typing.Rect2d) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    pt1 = (int(roi[0]), int(roi[1]))
    pt2 = (int(roi[0] + roi[2]), int(roi[1] + roi[3]))
    return pt1, pt2


def signed_area(a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float]) -> float:
    [a1, a2] = a
    [b1, b2] = b
    [c1, c2] = c

    return (b1*c2 + a1*b2 + c1*a2 - b1*a2 - b2*c1 - a1*c2)/2.0


def y_min(s: List[Tuple[float, float]]) -> Tuple[float, float]:
    return min(s, key=lambda x: [x[1], x[0]])


def y_max(s: List[Tuple[float, float]]) -> Tuple[float, float]:
    return max(s, key=lambda x: [x[1], x[0]])
