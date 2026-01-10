import numpy as np
import cv2


class FPS():
    def __init__(self, frames: int = 5) -> None:
        self.frames = frames
        self.times = []

    def add_frame(self, time: float) -> None:
        self.times.append(time)

    def calculate_fps(self) -> float:
        return 1/np.mean(self.times, dtype=float)

    def show_fps(self, frame: cv2.typing.MatLike) -> cv2.typing.MatLike:
        fps = self.calculate_fps()
        cv2.putText(frame, f'{int(np.ceil(fps))} FPS', (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 0, 0), 2, cv2.LINE_AA)
        return frame

    def update(self, frame: cv2.typing.MatLike, deltatime: float) -> cv2.typing.MatLike:
        if len(self.times) > self.frames:
            self.times.pop(0)

        self.add_frame(deltatime)

        frame = self.show_fps(frame)

        return frame
