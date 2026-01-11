import cv2
from threading import Thread
import time
from typing import Tuple, Union


class ThreadedCamera:
    def __init__(self, src=0, width=1280, height=720) -> None:
        self.capture = cv2.VideoCapture(src, cv2.CAP_DSHOW)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.status = False
        self.frame = None

        self.online = True
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

        

    def update(self) -> None:
        while self.online:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
            else:
                time.sleep(0.05)

    def read(self) -> Tuple[bool, Union[cv2.typing.MatLike, None]]:
        if self.frame is not None:
            return True, self.frame
        return False, None

    def release(self) -> None:
        self.capture.release()
        self.online = False
