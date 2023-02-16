#!/usr/bin/env python3
"""A basic cellular automata cave generation example using SciPy.

http://www.roguebasin.com/index.php?title=Cellular_Automata_Method_for_Generating_Random_Cave-Like_Levels

This will print the result to the console, so be sure to run this from the
command line.
"""
from typing import Any

import numpy as np
import scipy.signal  # type: ignore
from numpy.typing import NDArray
import tcod


def convolve(tiles: NDArray[Any], wall_rule: int = 5) -> NDArray[np.bool_]:
    """Return the next step of the cave generation algorithm.

    `tiles` is the input array. (0: wall, 1: floor)

    If the 3x3 area around a tile (including itself) has `wall_rule` number of
    walls then the tile will become a wall.
    """
    # Use convolve2d, the 2nd input is a 3x3 ones array.
    neighbors: NDArray[Any] = scipy.signal.convolve2d(tiles == 0, [[1, 1, 1], [1, 1, 1], [1, 1, 1]], "same")
    next_tiles: NDArray[np.bool_] = neighbors < wall_rule  # Apply the wall rule.
    return next_tiles


def show(tiles: NDArray[Any]) -> None:
    """Print out the tiles of an array."""
    for line in tiles:
        print("".join("# "[int(cell)] for cell in line))

noise = tcod.noise.Noise(
    dimensions=2,
    algorithm=tcod.noise.Algorithm.SIMPLEX,
    implementation=tcod.noise.Implementation.FBM,
    lacunarity=3.0,
    octaves=1.5,
    seed=69
    )


if __name__ == "__main__":
    WIDTH, HEIGHT = 120, 28
    INITIAL_CHANCE = 0.42  # Initial wall chance.
    INITIAL_RANGE = INITIAL_CHANCE / 2
    INITIAL_MIN = 0.5 - INITIAL_RANGE
    INITIAL_MAX = 0.5 + INITIAL_RANGE
    CONVOLVE_STEPS = 1
    WALL_RULE = 6
    noise_map = noise[tcod.noise.grid(shape=(WIDTH, HEIGHT), scale=0.25,)]
    noise_map = (noise_map + 1) * 0.5
    print(noise_map.min(), noise_map.max())
    # 0: wall, 1: floor
    tiles: NDArray[np.bool_] = np.all([noise_map <= INITIAL_MAX, noise_map >= INITIAL_MIN], axis=0)
    # tiles: NDArray[np.bool_] = noise_map <= INITIAL_CHANCE
    print(f"Walls: {np.count_nonzero(~tiles)}")
    print(noise_map.flags)
    print(tiles.dtype)
    for _ in range(CONVOLVE_STEPS):
        tiles = convolve(tiles, wall_rule=WALL_RULE)
    tiles[[0, -1], :] = 0  # Ensure surrounding wall.
    tiles[:, [0, -1]] = 0
    # show(tiles)
    # print(noise._seed())
    # print(noise_map.min(), noise_map.max())
