"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional

import tcod
from PIL import Image  # type: ignore
from pathlib import Path

import color
from engine import Engine
import entity_factories
from game_map import GameWorld
import input_handlers


# Load the background image and remove the alpha channel.
background_image = Image.open(Path("data/menu_background.png"))
if background_image.format != "RGB":
    background_image = background_image.convert("RGB")

# Load the title text.
title_text_file = open("data/SotM.txt", "r", encoding="UTF-8")
title_text = title_text_file.read()
title_text_file.close()


def new_game() -> Engine:
    """Return a brand new game session as an Engine instance."""

    map_width = 60
    map_height = 35

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
    )

    engine.game_world.generate_overworld()
    engine.update_fov()

    engine.message_log.add_message("Strike the earth!", color.welcome_text)

    # Starting equipment:
    dagger = copy.deepcopy(entity_factories.dagger)
    leather_armor = copy.deepcopy(entity_factories.leather_armor)

    dagger.parent = player.inventory
    leather_armor.parent = player.inventory

    player.inventory.items.append(dagger)
    player.equipment.toggle_equip(dagger, add_message=False)

    player.inventory.items.append(leather_armor)
    player.equipment.toggle_equip(leather_armor, add_message=False)

    return engine


def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine


class MainMenu(input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""

    def on_render(self, console: tcod.Console) -> None:
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            10,
            title_text,
            fg=color.title,
            alignment=tcod.CENTER,
        )

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "Survival on the Mountain",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "By TrialOrc",
            fg=color.menu_title,
            bg=color.black,
            alignment=tcod.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(["[N]ew game", "[C]ontinue last game", "[Q]uit"]):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

        for i, text in enumerate(["[N]", "[C]", "[Q]"]):
            console.print(
                console.width // 2 - (menu_width // 2) + 1,
                console.height // 2 - 2 + i,
                text.ljust(3),
                fg=color.highight_fg,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(0),
            )

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            try:
                return input_handlers.MainGameEventHandler(
                    load_game("sav/savegame.sav")
                )
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.K_n:
            return input_handlers.MainGameEventHandler(new_game())

        return None
