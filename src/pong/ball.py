from typing import List, Tuple


def updateBallPosition(present, vec) -> List[float]:
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


def calculate_collision_with_ball(p1: Tuple[int, int], p2: Tuple[int, int], ball_position):
    if (ball_position[0] > pt1[0]) and (ball_position[1] > pt1[1] and ball_position[1] < pt2[1]):

    if not changed_vec:
        if (ball_direction[0] - pt1[0] < ball_direction[1] - pt1[1]) or (ball_direction[0] - pt1[0] < ball_direction[1] - pt2[1]):
            ball_direction = rebound(ball_direction, "x")

        else:
            ball_direction = rebound(ball_direction, "y")
        changed_vec = True
    else:
        changed_vec = False

    return ball_direction
