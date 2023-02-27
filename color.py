from typing import Tuple
from PIL import Image


color_palette = Image.open("data/ColorPalette.png")
if color_palette.format != "RGB":
    color_palette = color_palette.convert("RGB")

tree_palette = Image.open("data/GrassTest.png")
if tree_palette.format != "RGB":
    tree_palette = tree_palette.convert("RGB")

white = color_palette.getpixel((8, 7))
black = color_palette.getpixel((0, 0))
red = color_palette.getpixel((3, 6))

player_atk = color_palette.getpixel((9, 0))
enemy_atk = color_palette.getpixel((7, 4))
needs_target = color_palette.getpixel((6, 1))
status_effect_applied = color_palette.getpixel((6, 0))
descend = color_palette.getpixel((5, 3))
ascend = color_palette.getpixel((13, 0))

player_die = color_palette.getpixel((5, 5))
enemy_die = color_palette.getpixel((5, 6))

invalid = color_palette.getpixel((10, 6))
impossible = color_palette.getpixel((10, 1))
error = color_palette.getpixel((4, 5))

welcome_text = color_palette.getpixel((5, 2))
health_recovered = color_palette.getpixel((5, 0))

bar_text = white
bar_filled = color_palette.getpixel((4, 0))
bar_empty = color_palette.getpixel((3, 6))

menu_title = color_palette.getpixel((12, 7))
menu_text = white
title = color_palette.getpixel((8, 0))

highight_fg = color_palette.getpixel((6, 7))
highlight_bg = color_palette.getpixel((15, 5))

corpse = color_palette.getpixel((3, 6))

orc = color_palette.getpixel((3, 1))
troll = color_palette.getpixel((2, 1))
duck = color_palette.getpixel((6, 6))

confusion_scroll = color_palette.getpixel((4, 4))
fireball_scroll = color_palette.getpixel((4, 6))
health_potion = color_palette.getpixel((3, 3))
lightning_scroll = color_palette.getpixel((4, 7))

weapon = color_palette.getpixel((6, 1))

armor = color_palette.getpixel((2, 7))

# np.random.randint(0,16)
# np.random.randint(0,8)

# Overworld
tree_light = color_palette.getpixel((2, 1))
tree_dark = color_palette.getpixel((0, 4))

ground_light = color_palette.getpixel((1, 1))
ground_dark = color_palette.getpixel((0, 2))

water_light = color_palette.getpixel((4, 3))
water_dark = color_palette.getpixel((0, 5))

blood_light = color_palette.getpixel((3, 6))
blood_dark = color_palette.getpixel((1, 7))


# Cave
cave_wall_light = color_palette.getpixel((3, 7))
cave_wall_dark = color_palette.getpixel((0, 7))

cave_floor_light = color_palette.getpixel((9, 6))
cave_floor_dark = color_palette.getpixel((15, 0))


def colorize_trees(x: float, y: float) -> Tuple[int, int, int]:
    y = int((y * x) * 256)
    x = int(x * 256)
    return tree_palette.getpixel((x, y))
