import cv2


def show_fps(frame: cv2.typing.MatLike, deltatime: float):
    cv2.putText(frame, f'{int(1/(deltatime))} FPS', (0, 20), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 0), 2, cv2.LINE_AA)
