import numpy as np
import cv2
import time


def detect_shape(contour):
    """
    Analyzes a contour to determine its geometric shape.
    Returns the name of the shape (Triangle, Square, Hexagon, Star, or undefined).
    """
    # 1. Calculate Perimeter
    perimeter = cv2.arcLength(contour, True)

    # 2. Approximate the polygon (simplify the shape)
    # Epsilon is the accuracy parameter. 0.04 (4%) is good for geometric shapes.
    approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)

    # 3. Count Corners (Vertices)
    corners = len(approx)

    shape_name = "Unknown"

    if corners == 3:
        shape_name = "Triangle"
    elif corners == 4:
        # Optional: Check aspect ratio to distinguish Square vs Rectangle
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = float(w) / h
        if 0.9 <= aspect_ratio <= 1.1:
            shape_name = "Square"
        else:
            shape_name = "Rectangle"
    elif corners == 5:
        shape_name = "Pentagon"
    elif corners == 6:
        shape_name = "Hexagon"
    elif corners > 8:
        # Stars usually have 10 corners (5 points + 5 inner valleys)
        # Also, stars are NOT convex (they have dents)
        if not cv2.isContourConvex(approx):
            shape_name = "Star"
        else:
            shape_name = "Circle"  # Or complex polygon

    return shape_name, approx


def run_detection():
    # Capturing video through webcam
    webcam = cv2.VideoCapture(0)

    # Kernel for noise removal (morphological operations)
    kernel = np.ones((5, 5), np.uint8)

    lasttime = time.perf_counter()

    while True:
        # FPS Calculation
        actual = time.perf_counter()
        deltatime = actual - lasttime
        lasttime = actual
        fps = int(1 / (deltatime if deltatime > 0 else 1))

        success, imageFrame = webcam.read()
        if not success:
            print("Failed to read from webcam")
            break

        # Convert to HSV
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

        # ==========================================
        # DEFINING COLOR MASKS
        # ==========================================

        # 1. RED MASK (Target: Triangle)
        # We combine two ranges: one for deep red (170-180) and one for your "terracotta" (0-20)
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([20, 255, 255])
        lower_red2 = np.array([170, 100, 100])
        upper_red2 = np.array([180, 255, 255])

        mask1 = cv2.inRange(hsvFrame, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsvFrame, lower_red2, upper_red2)
        red_mask = mask1 + mask2

        # 2. GREEN MASK (Target: Square)
        green_lower = np.array([25, 52, 72], np.uint8)
        green_upper = np.array([102, 255, 255], np.uint8)
        green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

        # 3. BLUE MASK (Target: Hexagon)
        blue_lower = np.array([94, 80, 2], np.uint8)
        blue_upper = np.array([120, 255, 255], np.uint8)
        blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

        # 4. ORANGE MASK (Target: Star)
        # Note: Starts at 20 to avoid overlapping too much with the Red Triangle
        orange_lower = np.array([20, 100, 100], np.uint8)
        orange_upper = np.array([40, 255, 255], np.uint8)
        orange_mask = cv2.inRange(hsvFrame, orange_lower, orange_upper)

        # ==========================================
        # PROCESSING LOOP
        # ==========================================

        # We store our targets in a list to avoid repeating code
        # Format: (Mask, Color Name, BGR Color for text, Expected Shape)
        tasks = [
            (red_mask, "Red", (0, 0, 255), "Triangle"),
            (green_mask, "Green", (0, 255, 0), "Square"),
            (blue_mask, "Blue", (255, 0, 0), "Hexagon"),
            (orange_mask, "Orange", (0, 165, 255), "Star")
        ]

        for mask, color_name, draw_color, expected_shape in tasks:

            # Clean up the mask (remove noise)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

            contours, _ = cv2.findContours(
                mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                area = cv2.contourArea(contour)

                # Filter small noise
                if area > 1000:
                    # Get the shape
                    detected_shape_name, approx_poly = detect_shape(contour)

                    # LOGIC CHECK:
                    # Only draw if the detected shape matches the expected shape for that color
                    # (Or if you want to see everything, remove the 'if' check below)

                    if detected_shape_name == expected_shape:
                        x, y, w, h = cv2.boundingRect(contour)

                        # Draw Rectangle
                        cv2.rectangle(imageFrame, (x, y),
                                      (x + w, y + h), draw_color, 2)

                        # Draw the actual contour polygon
                        cv2.drawContours(
                            imageFrame, [approx_poly], 0, (255, 255, 255), 2)

                        # Label Text
                        label = f"{color_name} {detected_shape_name}"
                        cv2.putText(imageFrame, label, (x, y - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, draw_color, 2)

        # Display FPS
        cv2.putText(imageFrame, f'FPS: {fps}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 255), 2)

        cv2.imshow("Shape & Color Detection", imageFrame)

        # Quit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    webcam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_detection()
