import cv2


class TransitionSystem:
    def __init__(self, duration: float) -> None:
        self.total_duration = duration
        self.elapsed_time = 0.0
        self.finished = False

    def update(self, frame: cv2.typing.MatLike, deltatime: float) -> cv2.typing.MatLike:
        self.elapsed_time += deltatime

        if self.elapsed_time >= self.total_duration:
            self.elapsed_time = self.total_duration
            self.finished = True

        progress = self.elapsed_time / self.total_duration

        height, width, _ = frame.shape

        bar_w = 400
        bar_h = 40
        center_x = width // 2
        center_y = height // 2

        top_left = (center_x - bar_w // 2, center_y - bar_h // 2)
        bottom_right = (center_x + bar_w // 2, center_y + bar_h // 2)

        fill_width = int(bar_w * progress)
        fill_bottom_right = (top_left[0] + fill_width, bottom_right[1])

        cv2.rectangle(frame, top_left, bottom_right, (200, 200, 200), 2)

        if fill_width > 0:
            cv2.rectangle(frame, top_left, fill_bottom_right,
                          (0, 255, 255), -1)

        text = f"CARGANDO PONG... {int(progress * 100)}%"
        cv2.putText(frame, text, (top_left[0], top_left[1] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        return frame
