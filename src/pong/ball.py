from typing import List, Tuple
import cv2
from constants import *
from utils import get_roi_points


class Ball:
    def __init__(self, position: List[float], direction: List[float]) -> None:
        self.position = position
        self.direction = direction
        self.changed_direction = False

    def update_position(self) -> None:
        self.position = [
            self.position[0] + self.direction[0],
            self.position[1] + self.direction[1],
        ]

    def rebound(self, axis: str) -> None:
        vx, vy = self.direction[0], self.direction[1]

        if axis == "x":
            vx = -vx
        elif axis == "y":
            vy = -vy
        else:
            raise ValueError(f"Axis {axis} is not valid.")

        self.direction = [vx, vy]

    def check_collision(self, roi: cv2.typing.Rect2d) -> bool:
        p1, p2 = get_roi_points(roi)

        if not (self.position[0] > p1[0] and self.position[0] < p2[0]):
            return False

        if not (self.position[1] > p1[1] and self.position[1] < p2[1]):
            return False

        return True

    def update_collision(self, roi: cv2.typing.Rect2d) -> None:
        p1, p2 = get_roi_points(roi)

        if not self.changed_direction:
            relative_pos_x = self.position[0] - p1[0]
            if (relative_pos_x < self.position[1] - p1[1]) or (
                relative_pos_x < self.position[1] - p2[1]
            ):
                self.rebound("x")
            else:
                self.rebound("y")
            self.changed_direction = True
        else:
            self.changed_direction = False

    def check_bounding_box_collision(self) -> None:
        if (
            self.position[0] > WINDOW_WIDTH - COLLISION_MARGIN
            or self.position[0] < COLLISION_MARGIN
        ):
            self.rebound("x")

        if (
            self.position[1] > WINDOW_HEIGHT - COLLISION_MARGIN
            or self.position[1] < COLLISION_MARGIN
        ):
            self.rebound("y")

    def draw(
        self,
        frame: cv2.typing.MatLike,
        radius: int = 10,
        color: Tuple[int, int, int] = (0, 0, 255),
        thickness: int = -1,
    ) -> cv2.typing.MatLike:
        position = (int(self.position[0]), int(self.position[1]))
        cv2.circle(frame, position, radius, color=color, thickness=thickness)
        return frame
