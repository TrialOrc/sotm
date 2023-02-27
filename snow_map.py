from __future__ import annotations
from typing import TYPE_CHECKING

import tcod
import numpy as np

from noise_factories import noise_perlin
import tile_types

if TYPE_CHECKING:
    from game_map import GameMap
    from numpy.typing import NDArray


class SnowMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snow_map = self.initialize_snow_map()

    def initialize_snow_map(self) -> NDArray:
        self.snow_map = noise_perlin[
            tcod.noise.grid(shape=(self.width, self.height), scale=0.25, indexing="xy")
        ].transpose()  # create a noise grid
        self.snow_map = self.snow_map + abs(self.snow_map.min())
        self.snow_map = self.snow_map * (
            8 / self.snow_map.max()
        )  # Normalize to 0.0 - 8.0
        return self.snow_map

    def get_value(self, x: int, y: int) -> float:
        return self.snow_map[x, y]

    def set_value(self, x: int, y: int, value: float):
        self.snow_map[x, y] = value

    def modify_value(self, x: int, y: int, value: float):
        self.snow_map[x, y] += value

    def modify_array(self, value: float) -> NDArray:
        self.snow_map = self.snow_map + value
        return self.snow_map

    def get_array(self):
        return self.snow_map

    def set_array(self, array: NDArray):
        self.snow_map = array

    def set_snow_levels(self, dungeon: GameMap, noise_map: np.ndarray):
        low_mask = np.logical_and(self.snow_map >= 1, self.snow_map < 3)
        med_mask = np.logical_and(self.snow_map >= 3, self.snow_map < 6)
        high_mask = np.logical_and(self.snow_map >= 6, self.snow_map < 8)
        max_mask = self.snow_map == 8

        for tile_type, mask in (
            (tile_types.snow_low, low_mask),
            (tile_types.snow_med, med_mask),
            (tile_types.snow_high, high_mask),
            (tile_types.snow_max, max_mask),
        ):
            indices = np.where(mask & noise_map)
            dungeon.tiles[indices] = tile_type
