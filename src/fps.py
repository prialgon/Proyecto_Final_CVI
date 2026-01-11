import numpy as np
import cv2
import time


class FPS():
    def __init__(self, max_fps: float, historic_frames: int = 5) -> None:
        self.frames = historic_frames
        self.times = []
        self.max_fps = max_fps

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

    def limit(self, deltatime: float) -> float:
        if deltatime < 1/self.max_fps:
            time.sleep(1/self.max_fps - deltatime)
            return 1/self.max_fps
        else:
            return deltatime
