import cv2
from typing import Tuple


def add_text(frame: cv2.typing.MatLike, text: str, position: str, size: float = 1, color: Tuple[int, int, int] = (0, 0, 0), thickness: int = 2) -> cv2.typing.MatLike:

    text_width, text_height = cv2.getTextSize(
        text, cv2.FONT_HERSHEY_SIMPLEX, size, 2)[0]

    if position == "top":
        TopCoordinates = (int(frame.shape[1] / 2) - int(text_width / 2),
                          50 + int(text_height / 2))
        cv2.putText(frame, text, TopCoordinates, cv2.FONT_HERSHEY_SIMPLEX,
                    size, color, thickness, cv2.LINE_AA)
    elif position == "top2":
        TopCoordinates = (int(frame.shape[1] / 2) - int(text_width / 2),
                          150 + int(text_height / 2))
        cv2.putText(frame, text, TopCoordinates, cv2.FONT_HERSHEY_SIMPLEX,
                    size, color, thickness, cv2.LINE_AA)
    elif position == "top3":
        TopCoordinates = (int(frame.shape[1] / 2) - int(text_width / 2),
                          200 + int(text_height / 2))
        cv2.putText(frame, text, TopCoordinates, cv2.FONT_HERSHEY_SIMPLEX,
                    size, color, thickness, cv2.LINE_AA)
    elif position == "center":
        CenterCoordinates = (int(frame.shape[1] / 2) - int(text_width / 2),
                             int(frame.shape[0] / 2) + int(text_height / 2))
        cv2.putText(frame, text, CenterCoordinates, cv2.FONT_HERSHEY_SIMPLEX,
                    size, color, thickness, cv2.LINE_AA)

    elif position == "right_corner":
        cv2.putText(frame, text, (frame.shape[1] - text_width - 10, text_height + 10), cv2.FONT_HERSHEY_SIMPLEX,
                    size, color, thickness, cv2.LINE_AA)
    return frame
