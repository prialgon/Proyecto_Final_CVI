import cv2
from security_system.constants import *
from typing import Sequence, Tuple, List
import math


def get_contours(mask: cv2.typing.MatLike) -> Sequence[cv2.typing.MatLike]:
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def is_target_shape(
    target_shape: str, n_corners: int, aspect_ratio: float, solidity: float, ar_rotated: float
) -> bool:
    detected = False

    if target_shape == TRIANGLE:
        if n_corners == 3:
            if ar_rotated < 2.0:
                if 0.9 <= aspect_ratio <= 1.15:
                    detected = True

    elif target_shape == SQUARE:
        if n_corners == 4:
            # if 0.9 <= aspect_ratio <= 1.1:
            if ar_rotated < 1.2:
                if solidity > 0.9:
                    detected = True

    elif target_shape == PENTAGON:
        if n_corners == 5:
            if solidity > 0.8:
                detected = True

    elif target_shape == HEXAGON:
        if n_corners == 6:
            if solidity > 0.8:
                detected = True

    return detected


def draw_shape(
    frame: cv2.typing.MatLike,
    approx: cv2.typing.MatLike,
    target_shape: str,
    color: str,
    draw_color: Tuple[int, int, int],
    bounding_rect: Tuple[int, int, int, int],
) -> None:
    x, y, w, h = bounding_rect
    cv2.drawContours(frame, [approx], -1, draw_color, 4)
    cv2.rectangle(frame, (x, y), (x + w, y + h), draw_color, 2)
    cv2.putText(
        frame,
        f"{color} {target_shape}",
        (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        draw_color,
        2,
    )


def get_side_lengths(approx: cv2.typing.MatLike) -> List[float]:
    sides = []
    for i in range(len(approx)):
        p1 = approx[i][0]
        p2 = approx[(i+1) % len(approx)][0]
        length = math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        sides.append(length)
    return sides


def detect_shapes(
    frame: cv2.typing.MatLike,
    contours: Sequence[cv2.typing.MatLike],
    target_shape: str,
    color: str,
    draw_color: Tuple[int, int, int],
    draw: bool = True,
) -> List[cv2.typing.MatLike]:
    shapes_detected = []
    for contour in contours:
        area = cv2.contourArea(contour)

        # Area threshold to not detect shapes caused by noise
        if area > SHAPE_AREA:
            perimeter = cv2.arcLength(contour, IS_CLOSED)

            epsilon = PERIMETER_CONSTANT * perimeter
            approx = cv2.approxPolyDP(contour, epsilon, IS_CLOSED)

            n_corners = len(approx)

            # All shapes are convex, we can use convex hull
            hull = cv2.convexHull(contour)
            hull_area = cv2.contourArea(hull)

            if hull_area == 0:
                continue

            solidity = float(area / hull_area)

            rect = cv2.minAreaRect(contour)
            (w_rect, h_rect) = rect[1]

            if w_rect == 0 or h_rect == 0:
                continue

            ar_rotated = max(w_rect, h_rect) / min(w_rect, h_rect)

            sides = get_side_lengths(approx)

            if not sides:
                continue

            max_side = max(sides)
            min_side = min(sides)

            aspect_ratio = max_side / min_side

            detected = is_target_shape(
                target_shape, n_corners, aspect_ratio, solidity, ar_rotated)

            if detected:
                x, y, w, h = cv2.boundingRect(approx)
                shapes_detected.append((target_shape, color, (x, y, w, h)))
                if draw:
                    draw_shape(
                        frame, approx, target_shape, color, draw_color, (
                            x, y, w, h)
                    )

    return shapes_detected
