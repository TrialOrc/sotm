from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

import numpy as np
from game_map import GameMap

if TYPE_CHECKING:
    from game_map import GameWorld

class Chunker:
    def __init__(self):
        self.chunks = {}

    def create_chunks(self, game_world: np.ndarray, width: int, height: int):
        for x in range(0, game_world.map_width, width):
            for y in range(0, game_world.map_height, height):
                self.chunks[(x//width, y//height)] = game_world[x:x+width, y:y+height]
