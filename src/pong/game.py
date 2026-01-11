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
            frame = self.kcf_player.draw_box(frame)
            self.ball.update_paddle_collisions(self.kcf_player.roi)
            if self.kcf_player.detected:
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
        if self.recalibrate_timer > 0:
            self.recalibrate_timer -= deltatime

        if self.recalibrate_timer <= 0 and self.recalibrate_timer != -100:
            self.kcf_player = Tracker(frame, 900, 1280, 0, 720, "right")
            self.trained = True

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
        self.points = 0

        self.togglePlayer = True

    def update(self, frame, deltatime):
        # ---------- RIGHT PLAYER ----------

        if not self.trained_right and not self.trained_left:
            frame = add_text(frame, "Place your hands in the red squares", "top")
            frame = add_text(
                frame, f"{int(self.recalibrate_left)}", "center", 5)
            frame = cv2.rectangle(
                frame, (1000, 200), (1280, 480),
                (0, 0, 255), 2
            )
            frame = cv2.rectangle(
                frame, (0, 200), (280, 480),
                (0, 0, 255), 2
            )

        else:
            if self.trained_right:
                if self.togglePlayer:
                    self.kcf_right.update(frame, 900, 1280, 0, 720)
                frame = self.kcf_right.draw_box(frame)
                self.ball.update_paddle_collisions(self.kcf_right.roi)
                if self.kcf_right.detected:
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
                if not self.togglePlayer:
                    self.kcf_left.update(frame, 0, 380, 0, 720)
                frame = self.kcf_left.draw_box(frame)
                self.ball.update_paddle_collisions(self.kcf_left.roi)
                if self.kcf_left.detected:
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
                        "top2"
                    )

        # ---------- AUTO RECALIBRATION ----------
        if self.recalibrate_right > 0:
            self.recalibrate_right -= deltatime
        
        if self.recalibrate_right <= 0 and self.recalibrate_right != -100:
            self.kcf_right = Tracker(frame, 900, 1280, 0, 720, "right")
            self.trained_right = True
            # self.recalibrate_right = -100

        if self.recalibrate_left > 0:
            self.recalibrate_left -= deltatime
        
        if self.recalibrate_left <= 0 and self.recalibrate_left != -100:
            self.kcf_left = Tracker(frame, 0, 380, 0, 720, "left")
            self.trained_left = True
            # self.recalibrate_left = -100

        # ---------- BALL ----------
        if self.trained_left and self.trained_right:
            self.points = self.ball.update_position()
            frame = self.ball.draw(frame)

        # ---------- SCORE ----------
        if self.points > 0:
            self.score_right += self.points
        elif self.points < 0:
            self.score_left += abs(self.points)

        if self.points != 0:
            self.ball.reset_position()

        frame = show_score(frame, self.score_left, self.score_right)
        self.togglePlayer = not self.togglePlayer
        return frame
