from typing import Tuple
import random

import numpy as np

import color

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch",np.int32), # Unicode codepoint.
        ("fg", "3B"), # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", bool), # True if this tile can be walked over.
        ("transparent", bool), # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),  # Graphics for when the tile is in FOV.
    ]
)

def new_tile(
    *,   # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
) -> np.ndarray:
    """Helper function for defining individual tile types."""
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

# SHROUD represents enexplored, unseen tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), color.cave_floor_dark),
    light=(ord(" "), (255, 255, 255), color.cave_floor_light),
)
wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord(" "), (255, 255, 255), color.cave_wall_dark),
    light=(ord(" "), (255, 255, 255), color.cave_wall_light),
)
tree = new_tile(
    walkable=False,
    transparent=False,
    dark=(ord("♠"), color.tree_dark, color.ground_dark),
    light=(ord("♠"), color.tree_light, color.ground_light),
)
ground = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), color.ground_dark),
    light=(ord(" "), (255, 255, 255), color.ground_light),
)

snow_low = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("░"), (87, 146, 218), color.ground_dark),
    light=(ord("░"), (255, 255, 255), color.ground_light),
)
snow_med = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("▒"), (87, 146, 218), color.ground_dark),
    light=(ord("▒"), (255, 255, 255), color.ground_light),
)
snow_high = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("▓"), (87, 146, 218), color.ground_dark),
    light=(ord("▓"), (255, 255, 255), color.ground_light),
)
snow_max = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord(" "), (87, 146, 218), color.ground_dark),
    light=(ord(" "), (255, 255, 255), (255, 255, 255)),
)

water_tile = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), color.ground_dark),
    light=(ord(" "), (255, 255, 255), color.ground_light),
)
blood_tile = new_tile(
    walkable=False,
    transparent=True,
    dark=(ord(" "), (255, 255, 255), color.ground_dark),
    light=(ord(" "), (255, 255, 255), color.ground_light),
)

down_stairs = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("∩"), color.cave_wall_dark, color.cave_floor_dark),
    light=(ord("∩"), color.cave_wall_light, color.cave_floor_light)
)