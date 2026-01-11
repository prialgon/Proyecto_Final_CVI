import numpy as np

# # Red Masks
# RED_MASK_LOW = np.array([[0, 120, 70], [10, 255, 255]])
# RED_MASK_HIGH = np.array([[170, 120, 70], [180, 255, 255]])

# # Green Masks
# GREEN_MASK = np.array([[40, 70, 70], [85, 255, 255]])

# # Blue Masks
# BLUE_MASK = np.array([[90, 100, 70], [125, 255, 255]])

# # Purple Masks
# PURPLE_MASK = np.array([[130, 80, 70], [160, 255, 255]])

# RED
RED_MASK_LOW = (np.array([0, 110, 70]), np.array([10, 255, 255]))
RED_MASK_HIGH = (np.array([165, 110, 70]), np.array([180, 255, 255]))

# GREEN
GREEN_MASK = (np.array([45, 100, 70]), np.array([85, 255, 255]))

# BLUE
BLUE_MASK = (np.array([90, 100, 70]), np.array([125, 255, 255]))

# PURPLE
# PURPLE_MASK = (np.array([125, 100, 70]), np.array([160, 255, 255]))
PURPLE_MASK = (np.array([144, 160, 99]), np.array([174, 255, 166]))


# Calibrated masks
# Green: Lower=[ 66 136 134], Upper=[ 82 255 255]
# GREEN_MASK = (np.array([66, 136, 134]), np.array([82, 255, 255]))

# Purple: Lower=[ 69 153 138], Upper=[179 255 255]

# Red: Lower=[160 129 165], Upper=[179 255 255]
# RED_MASK_LOW = RED_MASK_HIGH = (
#     np.array([160, 129, 165]), np.array([179, 255, 255]))
