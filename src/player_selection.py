from typing import Tuple, Union
import cv2
import time


class PlayerSelector:
    def __init__(self, selection_time: float, learning_rate: float = 0.3) -> None:
        self.selection_time = selection_time
        self.gamemode = 0
        self.finished = False
        self.learning_rate = learning_rate

        self.width = 400
        self.height = 300
        self.x_left = 200
        self.x_right = 700
        self.y = 200

        self.current_choice = 0
        self.start_time = None

        self.mog = cv2.createBackgroundSubtractorMOG2(
            history=300,
            varThreshold=50,
            detectShadows=False
        )
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        self.prev_hand_pos = None

    def get_hand_position(self, frame) -> Union[None, Tuple[int, int]]:
        foreground = self.mog.apply(frame)

        foreground = cv2.morphologyEx(foreground, cv2.MORPH_OPEN, self.kernel)
        foreground = cv2.morphologyEx(foreground, cv2.MORPH_CLOSE, self.kernel)

        contours, _ = cv2.findContours(
            foreground, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return None

        hand = max(contours, key=cv2.contourArea)
        if cv2.contourArea(hand) < 5000:
            return None

        M = cv2.moments(hand)

        if M["m00"] == 0:
            return None

        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        if self.prev_hand_pos:
            cx = int((1-self.learning_rate) *
                     self.prev_hand_pos[0] + self.learning_rate * cx)
            cy = int((1-self.learning_rate) *
                     self.prev_hand_pos[1] + self.learning_rate * cy)

        self.prev_hand_pos = (cx, cy)
        return (cx, cy)

    def is_in_box(self, hand_x, hand_y, box_x) -> bool:
        return (
            box_x <= hand_x <= box_x + self.width and
            self.y <= hand_y <= self.y + self.height
        )

    def update(self, frame) -> None:
        if self.finished:
            return

        if self.start_time and (time.time() - self.start_time) >= self.selection_time:
            self.gamemode = self.current_choice
            self.finished = True

        hand_pos = self.get_hand_position(frame)

        if hand_pos is None:
            return

        hand_x, hand_y = hand_pos

        in_left = self.is_in_box(hand_x, hand_y, self.x_left)
        in_right = self.is_in_box(hand_x, hand_y, self.x_right)

        selected = None
        if in_left:
            selected = 1
        elif in_right:
            selected = 2

        if selected != self.current_choice:
            self.current_choice = selected
            self.start_time = time.time() if selected else None

    def draw_bar(self, frame, box_x) -> None:
        if self.start_time is None:
            return

        elapsed = time.time() - self.start_time
        ratio = min(elapsed / self.selection_time, 1.0)

        bar_width = int(self.width * ratio)
        cv2.rectangle(
            frame,
            (box_x, self.y + self.height + 10),
            (box_x + bar_width, self.y + self.height + 30),
            (0, 255, 0),
            -1
        )

    def draw(self, frame) -> cv2.typing.MatLike:
        # Boxes
        cv2.rectangle(frame, (self.x_left, self.y),
                      (self.x_left + self.width, self.y + self.height),
                      (255, 255, 255), 2)

        cv2.rectangle(frame, (self.x_right, self.y),
                      (self.x_right + self.width, self.y + self.height),
                      (255, 255, 255), 2)

        # Labels
        cv2.putText(frame, "1 PLAYER",
                    (self.x_left + 100, self.y + 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.putText(frame, "2 PLAYERS",
                    (self.x_right + 80, self.y + 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Highlight + progress
        if self.current_choice == 1:
            cv2.rectangle(frame, (self.x_left, self.y),
                          (self.x_left + self.width, self.y + self.height),
                          (0, 255, 0), 4)
            self.draw_bar(frame, self.x_left)

        elif self.current_choice == 2:
            cv2.rectangle(frame, (self.x_right, self.y),
                          (self.x_right + self.width, self.y + self.height),
                          (0, 255, 0), 4)
            self.draw_bar(frame, self.x_right)

        # Hand debug
        if self.prev_hand_pos:
            cv2.circle(frame, self.prev_hand_pos, 12, (0, 0, 255), -1)

        return frame
