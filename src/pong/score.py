import cv2
from pong.text_manager import add_text


def show_score(frame: cv2.typing.MatLike, player_left_score: int, player_right_score: int) -> cv2.typing.MatLike:
    text = f"{player_left_score} | {player_right_score}"

    frame = add_text(frame, text, "top", 3, (255, 255, 255), 5)

    return frame
