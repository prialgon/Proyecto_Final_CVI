import os
from auxiliary import *
import cv2
from constants import CHESSBOARD_INNER_CORNERS_SIZE, CHESSBOARD_SQUARE_SIZE
import copy
from typing import List
import numpy as np

calibration_img_path = "../data/left"


def find_corners(imgs: List[cv2.typing.MatLike]) -> List[tuple[bool, cv2.typing.MatLike]]:
    corners = [cv2.findChessboardCorners(
        img, CHESSBOARD_INNER_CORNERS_SIZE) for img in imgs]

    return corners


def filter_corner_detections(corners: List[tuple[bool, cv2.typing.MatLike]]) -> List[cv2.typing.MatLike]:
    valid_corners = []
    for cor in corners:
        if cor[0]:
            valid_corners.append(cor)

    return valid_corners


def refine_corners(imgs_gray: List[cv2.typing.MatLike], corners: List[cv2.typing.MatLike]) -> List[cv2.typing.MatLike]:
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01)

    corners_refined = []
    for i, cor in zip(imgs_gray, corners):
        corner_refined = cv2.cornerSubPix(
            i, cor[1], CHESSBOARD_INNER_CORNERS_SIZE, (-1, -1), criteria)

        corners_refined.append(corner_refined)

    return corners_refined


if __name__ == "__main__":
    # Compute paths to images
    full_path = os.path.join(os.getcwd(), calibration_img_path)
    imgs_path = [os.path.join(full_path, i)
                 for i in os.listdir(full_path)]

    # Load images
    imgs = load_images(imgs_path)
    img_size = imgs[0].shape

    # Get gray images
    imgs_gray = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in imgs]

    # Find corners
    corners = find_corners(imgs)

    # Keep only valid detections
    valid_corners = filter_corner_detections(corners)

    # Refine corner detection
    valid_corners_copy = copy.deepcopy(valid_corners)

    # Get real chessboard points
    chessboard_points = [get_chessboard_points(
        CHESSBOARD_INNER_CORNERS_SIZE, CHESSBOARD_SQUARE_SIZE, CHESSBOARD_SQUARE_SIZE) for _ in range(len(valid_corners_copy))]

    # Get calibration parameters
    valid_corners = np.asarray(valid_corners, dtype=np.float32)

    rms, intrinsics, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        chessboard_points, valid_corners, img_size, None, None)

    # Obtain extrinsics
    extrinsics = list(map(lambda rvec, tvec: np.hstack(
        (cv2.Rodrigues(rvec)[0], tvec)), rvecs, tvecs))

    # Print calibration parameters
    print("Intrinsics:\n", intrinsics)
    print("Distortion coefficients:\n", dist_coeffs)
    print("Root mean squared reprojection error:\n", rms)
