import cv2
from pong.ball import Ball
from pong.constants import *
from pong.tracker import Tracker, AutoTracker
from pong.text_manager import add_text
from pong.score import show_score


from pong.score import show_score


class PongGame1P:
    def __init__(self, ball: Ball, kcf_auto: AutoTracker) -> None:
        self.kcf_player = None
        self.kcf_auto = kcf_auto
        self.ball = ball

        self.trained = False
        self.recalibrate_timer = 5

        # --- Scores ---
        self.player_score = 0
        self.ai_score = 0
        self.points = 0

    def update(self, frame, deltatime) -> cv2.typing.MatLike:
        # ---------- PLAYER TRACKING ----------
        if self.trained and self.kcf_player:
            self.kcf_player.update(frame, 900, 1280, 0, 720)

            if self.kcf_player.detected:
                frame = self.kcf_player.draw_box(frame)
                self.ball.update_paddle_collisions(self.kcf_player.roi)
                self.recalibrate_timer = -100
            else:
                if self.recalibrate_timer < 0:
                    self.recalibrate_timer = 5

                frame = cv2.rectangle(
                    frame, (1000, 200), (1280, 480),
                    (0, 0, 255), 2
                )
                frame = add_text(
                    frame,
                    f"Recalibrating in {int(self.recalibrate_timer)}",
                    "top"
                )

        else:
            frame = add_text(frame, "Place your hand in the red square", "top")
            frame = add_text(
                frame, f"{int(self.recalibrate_timer)}", "center", 5)
            frame = cv2.rectangle(
                frame, (1000, 200), (1280, 480),
                (0, 0, 255), 2
            )

        # ---------- AUTO TRAIN ----------
        if not self.trained:
            self.recalibrate_timer -= deltatime
            if self.recalibrate_timer <= 0:
                self.kcf_player = Tracker(frame, 900, 1280, 0, 720, "right")
                self.trained = True
                self.recalibrate_timer = -100

        # ---------- AI + BALL ----------
        if self.trained:
            self.kcf_auto.update(self.ball.y)
            self.ball.update_paddle_collisions(self.kcf_auto.roi)

            self.points = self.ball.update_position()
            frame = self.ball.draw(frame)

        frame = self.kcf_auto.draw_box(frame)

        # ---------- SCORING ----------
        if self.points > 0:
            self.player_score += self.points
        elif self.points < 0:
            self.ai_score += abs(self.points)

        if self.points != 0:
            self.ball.reset_position()

        show_score(frame, self.ai_score, self.player_score)

        return frame


class PongGame2P:
    def __init__(self, ball: Ball, kcf_auto: AutoTracker) -> None:
        self.kcf_auto = kcf_auto
        self.ball = ball

        self.kcf_right = None
        self.kcf_left = None

        self.trained_right = False
        self.trained_left = False

        self.recalibrate_right = 5
        self.recalibrate_left = 5

        self.score_right = 0
        self.score_left = 0

    def train_next(self, frame):
        if not self.trained_right:
            self.kcf_right = Tracker(frame, 900, 1280, 0, 720, "right")
            self.trained_right = True
            self.recalibrate_right = -100
        elif not self.trained_left:
            self.kcf_left = Tracker(frame, 0, 380, 0, 720, "left")
            self.trained_left = True
            self.recalibrate_left = -100

    def update(self, frame, deltatime):
        # ---------- RIGHT PLAYER ----------
        if self.trained_right:
            self.kcf_right.update(frame, 900, 1280, 0, 720)

            if self.kcf_right.detected:
                frame = self.kcf_right.draw_box(frame)
                self.ball.update_paddle_collisions(self.kcf_right.roi)
                self.recalibrate_right = -100
            else:
                if self.recalibrate_right < 0:
                    self.recalibrate_right = 5

                frame = cv2.rectangle(
                    frame, (1000, 200), (1280, 480),
                    (0, 0, 255), 2
                )
                frame = add_text(
                    frame,
                    f"Right recalibrating in {int(self.recalibrate_right)}",
                    "top"
                )

        # ---------- LEFT PLAYER ----------
        if self.trained_left:
            self.kcf_left.update(frame, 0, 380, 0, 720)

            if self.kcf_left.detected:
                frame = self.kcf_left.draw_box(frame)
                self.ball.update_paddle_collisions(self.kcf_left.roi)
                self.recalibrate_left = -100
            else:
                if self.recalibrate_left < 0:
                    self.recalibrate_left = 5

                frame = cv2.rectangle(
                    frame, (0, 200), (280, 480),
                    (0, 0, 255), 2
                )
                frame = add_text(
                    frame,
                    f"Left recalibrating in {int(self.recalibrate_left)}",
                    "top"
                )

        # ---------- AUTO RECALIBRATION ----------
        if self.recalibrate_right > 0:
            self.recalibrate_right -= deltatime
        elif self.recalibrate_right == 0:
            self.kcf_right = Tracker(frame, 900, 1280, 0, 720, "right")
            self.recalibrate_right = -100

        if self.recalibrate_left > 0:
            self.recalibrate_left -= deltatime
        elif self.recalibrate_left == 0:
            self.kcf_left = Tracker(frame, 0, 380, 0, 720, "left")
            self.recalibrate_left = -100

        # ---------- BALL ----------
        points = self.ball.update_position()
        frame = self.ball.draw(frame)

        # ---------- SCORE ----------
        if points > 0:
            self.score_left += points
        elif points < 0:
            self.score_right += abs(points)

        if points != 0:
            self.ball.reset_position()

        frame = show_score(frame, self.score_left, self.score_right)

        return frame
