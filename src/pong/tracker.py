from typing import List
import cv2
from pong.constants import *
from pong.utils import get_roi_points
import numpy as np


class Tracker:
    def __init__(self, frame: cv2.typing.MatLike, x_low: int, x_high: int, y_low: int, y_high: int, name: str) -> None:
        self.tracker = cv2.legacy.TrackerKCF_create()

        self.offset_x = x_low

        self.y_high = y_high
        masked = frame[y_low:y_high, x_low:x_high]

        self.tracker.init(masked, TRACK_WINDOW)

        if name != "left" and name != "right":
            raise ValueError("Tracker name must be 'left' or 'right'.")

        self.name = name

        self.roi = TRACK_WINDOW
        self.detected = False

        self.paddle_img = cv2.imread(PADDLE_IMAGE)

        self.img_shape = self.paddle_img.shape[:-1]

        self.ref_x = x_high if name == "right" else x_low + self.img_shape[1]

    def update(self, frame: cv2.typing.MatLike, x_low: int, x_high: int, y_low: int, y_high: int) -> None:
        masked = frame[y_low:y_high, x_low:x_high]

        detected, roi = self.tracker.update(masked)

        if detected:
            x, y, w, h = roi
            roi = (self.ref_x - self.img_shape[1], y, self.img_shape[1], h)
            self.roi = roi
            self.detected = True
        else:
            self.detected = False

    def draw_box(self, frame: cv2.typing.MatLike, thickness: int = -1, color: int = 255) -> cv2.typing.MatLike:
        p1, p2 = get_roi_points(self.roi)
        newFrame = frame

        if p1[1] <= 0:
            newFrame[0:self.img_shape[0],
                     self.ref_x-self.img_shape[1]:self.ref_x] = self.paddle_img
        elif p2[1] >= self.y_high:
            newFrame[self.y_high-self.img_shape[0]:self.y_high,
                     self.ref_x-self.img_shape[1]:self.ref_x] = self.paddle_img
        else:
            newFrame[p1[1]:p2[1],
                     self.ref_x-self.img_shape[1]:self.ref_x] = self.paddle_img
        # frame = cv2.rectangle(frame, p1, p2, color, thickness)
        return newFrame


class AutoTracker:
    def __init__(self, x_low: int, x_high: int, y_low: int, y_high: int, name: str) -> None:

        self.offset_x = x_low

        self.y_high = y_high

        if name != "left" and name != "right":
            raise ValueError("Tracker name must be 'left' or 'right'.")

        self.name = name

        self.roi = TRACK_WINDOW

        self.paddle_img = cv2.imread(PADDLE_IMAGE)

        self.img_shape = self.paddle_img.shape[:-1]

        self.ref_x = x_high if name == "right" else x_low + self.img_shape[1]

        self.ball_history: List[float] = [
            (y_high + y_low) // 2 for _ in range(4)]

        self.max_speed = 10

        self.pos_y = (y_high + y_low) // 2

    def update(self, ball_y: float) -> None:
        self.ball_history.append(ball_y)
        ballpos = self.ball_history.pop(0) - self.img_shape[0] // 2
        next_pos = min(abs(self.pos_y - ballpos), self.max_speed)
        direction = np.sign(ballpos - self.pos_y)
        self.pos_y += direction*next_pos

        self.max_speed = np.random.normal(10.5, 3)

        roi = (self.ref_x - self.img_shape[1],
               self.pos_y, self.img_shape[1], 280)
        self.roi = roi

    def draw_box(self, frame: cv2.typing.MatLike, thickness: int = -1, color: int = 255) -> cv2.typing.MatLike:
        p1, p2 = get_roi_points(self.roi)
        newFrame = frame

        if p1[1] <= 0:
            newFrame[0:self.img_shape[0],
                     self.ref_x-self.img_shape[1]:self.ref_x] = self.paddle_img
        elif p2[1] >= self.y_high:
            newFrame[self.y_high-self.img_shape[0]:self.y_high,
                     self.ref_x-self.img_shape[1]:self.ref_x] = self.paddle_img
        else:
            newFrame[p1[1]:p2[1],
                     self.ref_x-self.img_shape[1]:self.ref_x] = self.paddle_img
        # frame = cv2.rectangle(frame, p1, p2, color, thickness)
        return newFrame
