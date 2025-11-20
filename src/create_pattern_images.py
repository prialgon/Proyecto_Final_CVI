from PIL import Image, ImageDraw
import os
import math

WORKDIR = os.getcwd()

patterns_path = "data/security_system_patterns"

figures_to_create = [("triangle", "red"), ("hexagon", "blue"),
                     ("square", "green"), ("star", "orange")]


def create_shape_image(shape, color, filename):
    # Create 1000x1000 white canvas
    img = Image.new("RGB", (1000, 1000), "white")
    draw = ImageDraw.Draw(img)

    # Padding
    pad = 100
    left, top = pad, pad
    right, bottom = 1000 - pad, 1000 - pad

    if shape == "triangle":
        points = [
            ((left + right)//2, top),  # top middle
            (left, bottom),           # bottom left
            (right, bottom)           # bottom right
        ]
        draw.polygon(points, fill=color)

    elif shape == "square":
        draw.rectangle([left, top, right, bottom], fill=color)

    elif shape == "hexagon":
        cx, cy = 500, 500
        r = 400  # radius
        points = []
        for i in range(6):
            angle = math.radians(60 * i - 90)
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.append((x, y))
        draw.polygon(points, fill=color)

    elif shape == "star":
        cx, cy = 500, 500
        r_outer = 400
        r_inner = 180
        points = []
        for i in range(10):
            angle = math.radians(i * 36 - 90)
            r = r_outer if i % 2 == 0 else r_inner
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            points.append((x, y))
        draw.polygon(points, fill=color)

    img.save(filename)


if __name__ == "__main__":
    path = os.path.join(WORKDIR, patterns_path)
    os.makedirs(path, exist_ok=True)

    for figure in figures_to_create:
        figure_type = figure[0]
        colour = figure[1]

        if figure_type not in ["triangle", "square", "hexagon", "star"]:
            print(f"{figure_type} is not allowed.")
            continue

        create_shape_image(figure_type, colour,
                           f"{path}/{colour}_{figure_type}.png")
