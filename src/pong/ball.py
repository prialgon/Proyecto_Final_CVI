from typing import List, Tuple
import cv2
from constants import *
from utils import *


class Ball:
    def __init__(
        self, position: List[float], direction: List[float], radius: int = 5
    ) -> None:
        self.x = position[0]
        self.y = position[1]
        self.vx = direction[0]
        self.vy = direction[1]

        self.radius = radius

        self.image = cv2.imread('data/small_ball_pixelart.png')

    def update_position(self) -> None:
        self.x += self.vx
        self.y += self.vy

        self.update_wall_collisions()

    def in_horizontal_edge(self, s: Tuple[Tuple[float, float], Tuple[float, float]]) -> bool:
        if not (min(s[0][0], s[1][0]) <= self.x <= max(s[0][0], s[1][0])):
            return False

        if signed_area(s[0], s[1], (self.x, self.y + self.radius)) * \
                signed_area(s[0], s[1], (self.x, self.y - self.radius)) <= 0:
            return True

        return False

    def in_vertical_edge(self, s: Tuple[Tuple[float, float], Tuple[float, float]]) -> bool:
        if not (min(s[0][1], s[1][1]) <= self.y <= max(s[0][1], s[1][1])):
            return False

        if signed_area(s[0], s[1], (self.x + self.radius, self.y))*signed_area(s[0], s[1], (self.x - self.radius, self.y)) <= 0:
            return True

        return False

    def update_wall_collisions(self) -> None:
        # Vertical axis wall collision
        if self.vx > 0:
            if self.x + self.radius > WINDOW_WIDTH:
                self.rebound("x")
        elif self.vx < 0:
            if self.x - self.radius < 0:
                self.rebound("x")

        # Horizontal axis wall collision
        if self.vy > 0:
            if self.y + self.radius > WINDOW_HEIGHT:
                self.rebound("y")
        elif self.vy < 0:
            if self.y - self.radius < 0:
                self.rebound("y")

    def rebound(self, axis: str) -> None:
        if axis == "x":
            self.vx *= -1
        elif axis == "y":
            self.vy *= -1
        else:
            raise ValueError(f"Axis {axis} is not valid.")

    def update_paddle_collisions(self, roi: cv2.typing.Rect2d) -> None:
        (xmin, ymin), (xmax, ymax) = get_roi_points(roi)

        if self.vx > 0:
            if self.in_vertical_edge(((xmin, ymin), (xmin, ymax))):
                self.x = xmin - self.radius
                self.rebound("x")
        elif self.vx < 0:
            if self.in_vertical_edge(((xmax, ymin), (xmax, ymax))):
                self.x = xmax + self.radius
                self.rebound("x")

        if self.vy > 0:
            if self.in_horizontal_edge(((xmin, ymin), (xmax, ymin))):
                self.y = ymin - self.radius
                self.rebound("y")
        elif self.vy < 0:
            if self.in_horizontal_edge(((xmin, ymax), (xmax, ymax))):
                self.y = ymax + self.radius
                self.rebound("y")

    def draw(
        self,
        frame: cv2.typing.MatLike,
        color: Tuple[int, int, int] = (0, 0, 255),
    ) -> cv2.typing.MatLike:
        position = (int(self.x), int(self.y))
        # cv2.circle(frame, position, self.radius, color=color, thickness=-1)

        newFrame = frame.copy()
        roi = newFrame[self.y-10:self.y+10, self.x-10:self.x+10]
        if all(i == 20 for i in roi.shape[:-1]) :
            newFrame[self.y-10:self.y+10, self.x-10:self.x+10] = self.image
        return newFrame
