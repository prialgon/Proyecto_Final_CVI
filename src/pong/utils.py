import cv2
from typing import Tuple


def get_roi_points(roi: cv2.typing.Rect2d) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    pt1 = (int(roi[0])+900, int(roi[1]))
    pt2 = (int(roi[0]+900 + roi[2]), int(roi[1] + roi[3]))
    return pt1, pt2


def show_fps(frame: cv2.typing.MatLike, deltatime: float) -> cv2.typing.MatLike:
    cv2.putText(frame, f'{int(1/(deltatime))} FPS', (0, 20), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 0), 2, cv2.LINE_AA)
    return frame
