import cv2
from constants import *
from utils import get_roi_points


class Tracker:
    def __init__(self, frame: cv2.typing.MatLike, x_low: int, x_high: int, y_low: int, y_high: int, name: str) -> None:
        self.tracker = cv2.legacy.TrackerKCF_create()

        self.offset_x = x_low

        masked = frame[y_low:y_high, x_low:x_high]

        self.tracker.init(masked, TRACK_WINDOW)

        if name != "left" and name != "right":
            raise ValueError("Tracker name must be 'left' or 'right'.")

        self.name = name

        self.roi = TRACK_WINDOW
        self.detected = False

    def update(self, frame: cv2.typing.MatLike, x_low: int, x_high: int, y_low: int, y_high: int) -> None:
        masked = frame[y_low:y_high, x_low:x_high]
        detected, roi = self.tracker.update(masked)

        if detected:
            x, y, w, h = roi
            roi = (x + self.offset_x, y, w, h)
            self.roi = roi
            self.detected = True
        else:
            self.detected = False

    def draw_box(self, frame: cv2.typing.MatLike, thickness: int = -1, color: int = 255) -> cv2.typing.MatLike:
        p1, p2 = get_roi_points(self.roi)
        frame = cv2.rectangle(frame, p1, p2, color, thickness)
        return frame
