from __future__ import annotations

from typing import TYPE_CHECKING

import tcod
import tcod.camera

if TYPE_CHECKING:
    from game_map import GameMap
    from entity import Actor

class Camera:
    def __init__(self, game_map: GameMap, player: Actor) -> None:
        self.game_map = game_map
        self.player = player
        
        self.width = game_map.width
        self.height = game_map.height
        self.x = player.x
        self.y = player.y

def camera(self, console):
    camera = tcod.camera.get_camera((self.width, self.height), (self.x, self.y))
    screen_view, world_view = tcod.camera.get_views(console, self.game_map, camera)
    return screen_view, world_view