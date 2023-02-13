from typing import Tuple
from math import sqrt, atan2, cos, sin, pi, pow
import numpy as np
import tcod


def sanity_loss(sanity: Tuple[int, int], direction: Tuple[int, int]) -> Tuple[int, int]:
    """
    This function takes a 2D point represented as a tuple of integers, `sanity`, and `direction` the direction of sanity loss.
    If the sanity loss continues in the same direction, the sanity loss will add direction values as normal.
    If the sanity loss goes in the opposite direction, the sanity loss will travel along a circle towards the direction of loss.
        This prevents sanity from being recovered by taking two conflicting sanity losses.
    Sanity loss will also ignore traveling in a circle if the distance from (0, 0) is > 2. This is a safe zone of sanity, and also causes
        issues with drawing a circle too small.
    """
    x, y = sanity
    dx, dy = direction
    if dx == 0 and dy == 0:  # If no movement return original value. Condition should never come up but this will catch any errors if it does.
        return sanity
    
    if ((np.sign(x) != np.sign(dx) and dy == 0)
        or (dx == 0 and np.sign(y) != np.sign(dy))
        or (np.sign(x) != np.sign(dx) and np.sign(y) != np.sign(dy))
    ):  # Catches direction not moving 'outward' away from (0, 0).
        radius = sqrt(x ** 2 + y ** 2)
        diameter = radius * 2
        distance = sqrt(dx ** 2 + dy ** 2)  # Calculates the distance from origin to end point.
        if radius > 2 or distance > radius * 2:
            pixel_degree = 147.86 * pow(diameter, -1.068)  # Calculates the degrees it takes to move 1 pixel.
            angle = atan2(y, x) + (pixel_degree * pi / 180) * (dx - dy)
            x = radius * cos(angle)
            y = radius * sin(angle)
        else:
            x = x + dx
            y = y + dy
    else:
        x += dx
        y += dy
    x = min(max(x, -10), 10)
    y = min(max(y, -10), 10)
    return (int(round(x, 0)), int(round(y, 0)))

print(sanity_loss((-4, -4), (0, 1)))

def sanity_recover(sanity: Tuple[int, int], recovered: int) -> Tuple[int, int]:
    x, y = sanity
    x += 10
    y += 10
    if not sanity == (0, 0):
        cost = np.ones((21, 21), dtype=np.int8, order="F")
        path = tcod.path.AStar(cost, diagonal=1).get_path(x, y, 10, 10)
        if recovered > len(path):
            return 0, 0
        else:
            x, y = path[recovered - 1]
            x -= 10
            y -= 10
            return x, y
    return sanity


def test_sanity_loss():
    x = 1
    y = 1
    for dx in range(-1, 3):
        for dy in range(-1, 3):
            if dx == 0 and dy == 0:
                continue
            sanity = (x, y)
            direction = (dx, dy)
            sanity_loss(sanity, direction)

# test_sanity_loss()