import cv2


def show_score(frame: cv2.typing.MatLike, player_left_score: int, player_right_score: int) -> cv2.typing.MatLike:
    text = f"{player_left_score} | {player_right_score}"

    frame = cv2.putText(
        frame, text, (frame.shape[1]//2 - len(text), 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    return frame
