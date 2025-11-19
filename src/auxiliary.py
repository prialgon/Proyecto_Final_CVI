from typing import List
import imageio
import cv2
import numpy as np
import numpy.typing


def load_images(filenames: List) -> List:
    return [imageio.imread(filename) for filename in filenames]


def show_image(img) -> None:
    cv2.imshow("Image", img)
    cv2.waitKey()
    cv2.destroyAllWindows()


def write_image(img, filename="img.jpg") -> None:
    cv2.imwrite(filename, img)


def get_chessboard_points(chessboard_shape, dx, dy) -> numpy.typing.NDArray:
    points = []
    for i in range(chessboard_shape[1]):
        for j in range(chessboard_shape[0]):
            points.append([j*dx, i*dy, 0])
    return np.asarray(points, dtype=np.float32)
