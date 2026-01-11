from typing import List, Tuple
import cv2
from pong.constants import *
from pong.utils import *
from random import uniform, choice
from math import atan2, cos, sin, hypot, radians, pi

ANGLE_PERTURBATION = radians(10)
SPEEDUP_CHANCE = 0.25
SPEEDUP_FACTOR = 1.1
MIN_SPEED = 6
MAX_SPEED = 22


class Ball:
    def __init__(
        self, position: List[float], direction: List[float], radius: int = 5
    ) -> None:
        self.x: float = position[0]
        self.y: float = position[1]
        self.vx: float = int(direction[0] * uniform(0.8, 1) * choice([-1, 1]))
        self.vy: float = int(direction[1] * uniform(0.8, 1) * choice([-1, 1]))

        self.initial = (position, direction)
        self.radius = radius

        self.image = cv2.imread(BALL_IMAGE, cv2.IMREAD_UNCHANGED)

        if self.image is None:
            raise ValueError("BALL IMAGE NOT FOUND")

    def update_position(self) -> int:
        self.x += self.vx
        self.y += self.vy

        points = self.update_wall_collisions()

        return points

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

    def update_wall_collisions(self) -> int:

        points = 0
        # Vertical axis wall collision
        if self.vx > 0:
            if self.x + self.radius > WINDOW_WIDTH:
                self.rebound("x")
                points = -1
        elif self.vx < 0:
            if self.x - self.radius < 0:
                self.rebound("x")
                points = 1

        # Horizontal axis wall collision
        if self.vy > 0:
            if self.y + self.radius > WINDOW_HEIGHT:
                self.rebound("y")
        elif self.vy < 0:
            if self.y - self.radius < 0:
                self.rebound("y")

        return points

    def rebound(self, axis: str) -> None:
        if axis == "x":
            self.vx *= -1
        elif axis == "y":
            self.vy *= -1
        else:
            raise ValueError(f"Axis {axis} is not valid.")

    def rebound_with_small_angle(self) -> None:
        # Compute current speed and angle
        speed = hypot(self.vx, self.vy)
        angle = atan2(self.vy, self.vx)

        # Flip horizontal direction (MANDATORY for bounce)
        angle = pi - angle

        # Small angle perturbation
        angle += uniform(-ANGLE_PERTURBATION, ANGLE_PERTURBATION)

        # Rare speed increase
        if uniform(0, 1) < SPEEDUP_CHANCE:
            speed *= SPEEDUP_FACTOR

        speed = max(MIN_SPEED, min(MAX_SPEED, speed))

        # New velocity
        vx = cos(angle) * speed
        vy = sin(angle) * speed

        # Convert to int safely
        self.vx = int(round(vx))
        self.vy = int(round(vy))

        # Safety guards
        if self.vx == 0:
            self.vx = 1 if vx > 0 else -1
        if self.vy == 0:
            self.vy = 1

    def update_paddle_collisions(self, roi: cv2.typing.Rect2d) -> None:
        (xmin, ymin), (xmax, ymax) = get_roi_points(roi)

        if self.vx > 0:
            if self.in_vertical_edge(((xmin, ymin), (xmin, ymax))):
                self.x = xmin - self.radius - 1
                self.rebound_with_small_angle()

        elif self.vx < 0:
            if self.in_vertical_edge(((xmax, ymin), (xmax, ymax))):
                self.x = xmax + self.radius + 1
                self.rebound_with_small_angle()

        # Top/bottom of paddle stays unchanged
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
        color: Tuple[int, int, int] = (0, 0, 255)
    ) -> cv2.typing.MatLike:

        # 1. Convert float coordinates to integers (Required for slicing)
        x_int = int(self.x)
        y_int = int(self.y)

        # 2. Get dimensions
        # 'h' is height, 'w' is width
        h, w, channels = self.image.shape
        frame_h, frame_w, _ = frame.shape

        # 3. Boundary Check (Prevents Crashing)
        # We check both positive overflow (> frame size) and negative (< 0)
        if (y_int + h > frame_h) or (x_int + w > frame_w) or (y_int < 0) or (x_int < 0):
            return frame

        # 4. Create copy to avoid modifying original frame by reference
        new_frame = frame.copy()

        # 5. Extract Region of Interest (ROI)
        # We use the integer coordinates here
        roi = new_frame[y_int:y_int+h, x_int:x_int+w]

        # 6. Prepare Blending Data
        ball_rgb = self.image[:, :, 0:3]
        alpha_channel = self.image[:, :, 3]

        # Normalize alpha to 0.0 - 1.0
        mask = alpha_channel / 255.0
        inv_mask = 1.0 - mask

        # 7. Blend the images
        for c in range(0, 3):
            roi[:, :, c] = (mask * ball_rgb[:, :, c] +
                            inv_mask * roi[:, :, c])

        # 8. Put the blended ROI back into the frame
        new_frame[y_int:y_int+h, x_int:x_int+w] = roi

        return new_frame

    def reset_position(self) -> None:
        self.x, self.y = self.initial[0]
        self.vx, self.vy = self.initial[1]
        self.vx = int(self.vx * uniform(0.8, 1) * choice([-1, 1]))
        self.vy = int(self.vy * uniform(0.8, 1) * choice([-1, 1]))
