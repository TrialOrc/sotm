from __future__ import annotations
from typing import TYPE_CHECKING

import numpy as np
import tcod

if TYPE_CHECKING:
    from game_map import GameWorld


class Chunker:
    """
    A class to handle converting the overworld map into chunks.
    """
    def __init__(self) -> None:
        self.chunks = {}

    def create_chunks(self, dungeon: GameWorld, width: int, height: int):
        # Possibly in a `dict[tuple[int, int], NDArray[Any]]`-like container.
        for x in range(0, dungeon.shape[0], width):
            for y in range(0, dungeon.shape[1], height):
                self.chunks[(x//width, y//height)] = dungeon[x:x+width, y:y+height]
