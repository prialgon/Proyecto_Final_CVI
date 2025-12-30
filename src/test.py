import cv2
import os
import numpy as np
import time


def main(camera_index=0, width=1280, height=720):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Could not open the camera (index {camera_index}).")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    window_name = "Live Camera - press 'q' to quit"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # resizable window

    # kf = kalman()

    # measurement = np.array((2, 1), np.float32)
    # prediction = np.zeros((2, 1), np.float32)
    trained = False

    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 30, 1)

    tracker = cv2.legacy.TrackerKCF()

    track_window = x, y, w, h = (200, 200, 1280-1000, 480-200)

    lasttime = time.time()-1

    ball_position = [10, 700]
    ball_direction = [14, -14]

    changed_vec = False

    try:
        while True:
            actual = time.time()

            deltatime = actual - lasttime

            lasttime = actual
            ret, frame = cap.read()
            if not ret:
                print("No frame received (the camera may have been disconnected).")
                break

            # Optional: flip horizontally (mirror), comment out if not desired
            frame = cv2.flip(frame, 1)

            # Wait 1 ms for a key; exit with 'q' or ESC
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
            elif key == ord('s'):

                kcf = tracker.create()
                # mask = np.zeros(frame.shape[:2], dtype="uint8")

                # mask = cv2.rectangle(mask, (800, 0), (1280, 720), 255,  -1)

                masked = frame[0:720, 900:1280]

                # masked = cv2.bitwise_and(frame, frame, mask=mask)
                kcf.init(masked, track_window)
                trained = True

                final_frame = frame

            elif trained:
                # mask = np.zeros(frame.shape[:2], dtype="uint8")

                # mask = cv2.rectangle(mask, (800, 0), (1280, 720), 255,  -1)
                # masked = cv2.bitwise_and(frame, frame, mask=mask)
                masked = frame[0:720, 900:1280]
                detected, roi = kcf.update(masked)
                pt1 = (int(roi[0])+900, int(roi[1]))

                pt2 = (int(roi[0]+900 + roi[2]), int(roi[1] + roi[3]))

                if detected:
                    rectframe = cv2.rectangle(frame, pt1, pt2, 255, -1)
                    if (ball_position[0] > pt1[0]) and (ball_position[1] > pt1[1] and ball_position[1] < pt2[1]):

                        if not changed_vec:
                            if (ball_direction[0] - pt1[0] < ball_direction[1] - pt1[1]) or (ball_direction[0] - pt1[0] < ball_direction[1] - pt2[1]):
                                ball_direction = rebound(ball_direction, "x")

                            else:
                                ball_direction = rebound(ball_direction, "y")
                            changed_vec = True
                        else:
                            changed_vec = False
                    cv2.putText(rectframe, f'{int(1/(deltatime))} FPS', (0, 20), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (255, 0, 0), 2, cv2.LINE_AA)
                    final_frame = rectframe
                else:
                    final_frame = frame
            else:
                frame = cv2.rectangle(
                    frame, (1000, 200), (1280, 480), color=(0, 0, 255), thickness=2)

                cv2.putText(frame, f'{int(1/(deltatime))} FPS', (0, 20), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 0, 0), 2, cv2.LINE_AA)

                final_frame = frame

                # Display the frame

            cv2.circle(final_frame, ball_position, 10,
                       color=(0, 0, 255), thickness=-1)
            cv2.imshow(window_name, final_frame)

            if ball_position[0] > 1275 or ball_position[0] < 5:

                ball_direction = rebound(ball_direction, "x")

            if ball_position[1] < 5 or ball_position[1] > 715:
                ball_direction = rebound(ball_direction, "y")

            ball_position = updateBallPosition(ball_position, ball_direction)

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()


def kalman():
    kf = cv2.KalmanFilter(4, 2)

    # TODO: Initialize the state of the Kalman filter
    dt = 1/30
    kf.measurementMatrix = np.array([[1, 0, 0, 0],
                                    # Measurement matrix np.array of shape (2, 4) and type np.float32
                                     [0, 1, 0, 0]], dtype=np.float32)
    kf.transitionMatrix = np.array([[1, 0, dt, 0],
                                    [0, 1, 0, dt],
                                    [0, 0, 1, 0],
                                    # Transition matrix np.array of shape (4, 4) and type np.float32
                                    [0, 0, 0, 1]], dtype=np.float32)
    # Process noise covariance np.array of shape (4, 4) and type np.float32
    kf.processNoiseCov = np.eye(4, dtype=np.float32) * 0.03

    return kf


"""
    measurement = np.array((2, 1), np.float32)
    prediction = np.zeros((2, 1), np.float32)

    # TODO: Show the frames to select the initial position of the object

    for i, frame in enumerate(frames):
        # Show the frame
        cv2.imshow('Frame', frame)
        # Wait for the key
        key = cv2.waitKey(0)
        # If the key is 'n' continue to the next frame
        if key == ord('n'):
            continue
        # If the key is 's' select the position of the object
        elif key == ord('s'):
            # Select the position of the object
            x, y, w, h = cv2.selectROI('Frame', frame, False)
            track_window = (x, y, w, h)
            # TODO: Compute the center of the object
            cx = x + w/2
            cy = y + h/2
            # TODO: Initialize the state of the Kalman filter
            kf.statePost = np.array([[cx], [cy], [0], [0]], np.float32)
            # Initialize the covariance matrix
            kf.errorCovPost = np.eye(4, dtype=np.float32)
            # Predict the position of the object
            prediction = kf.predict()

            # TODO: Update the measurement and correct the Kalman filter
            measurement = np.array([[cx], [cy]], np.float32)
            kf.correct(measurement)

            # TODO: Crop the object
            crop = frame[y:y+h, x:x+w].copy()
            hsv_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
            # TODO: Compute the histogram of the cropped object (Reminder: Use only the Hue channel (0-180))
            mask = cv2.inRange(hsv_crop,
                            np.array((0., 60., 32.)),
                            np.array((180., 255., 255.)))
            crop_hist = cv2.calcHist([hsv_crop], [0], mask=mask, histSize=[
                                    32], ranges=[0, 180])
            cv2.normalize(crop_hist, crop_hist, 0, 255, cv2.NORM_MINMAX)

            print(f'Initial position selected: {x}, {y}')
            break

    """


def updateBallPosition(present, vec):
    return [present[0] + vec[0], present[1] + vec[1]]


def rebound(vec, dir):
    vx, vy = vec

    if dir == "x":
        vx = -vx

    if dir == "y":
        vy = -vy
    # MOD = 10
    # angle = np.atan2(vec[1], vec[0])
    # print(f"angle: {angle}, {angle*(360/(2*np.pi))}")
    # new_angle = np.pi - angle
    # # print(new_angle)
    # new_vec = [np.intp(np.ceil(MOD * np.cos(new_angle))),
    #            np.intp(np.ceil(MOD * np.sin(new_angle)))]
    # print(new_vec)
    return vx, vy


if __name__ == "__main__":
    # If the built-in webcam is not at index 0, change the first argument: main(1)
    main(camera_index=0, width=1280, height=720)
