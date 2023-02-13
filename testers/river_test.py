from typing import List, Tuple
import tcod
import numpy as np

import time


def generate_river(map: np.ndarray, instance: int) -> List[Tuple[int, int]]:
    sorted_array = np.sort(map.flatten())
    value = sorted_array[-(instance + 1)]
    index = np.argwhere(map == value)
    mouth_x, mouth_y = index[0]
    
    # List to store the coordinates of the lowest values
    river_list = []
    river_list.append((mouth_x, mouth_y))

    # Start with the initial coordinates (x, y)
    current_coords = (mouth_x, mouth_y)

    while True:
        # Get the current value at the current coordinates
        current_value = map[current_coords]

        # Initialize the lowest value and lowest value coordinates to be the current value and coordinates
        lowest_value = current_value
        lowest_value_coords = current_coords

        # Check the values of the four cardinal directions.
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            # Get the coordinates of the neighboring cell
            neighbor_coords = (current_coords[0] + dx, current_coords[1] + dy)
            # Make sure the coordinates are within the bounds of the map array
            if neighbor_coords[0] < 0 or neighbor_coords[0] >= map.shape[0] or \
            neighbor_coords[1] < 0 or neighbor_coords[1] >= map.shape[1]:
                continue
            # Get the value at the neighboring cell
            neighbor_value = map[neighbor_coords]
            # Update the lowest value and lowest value coordinates if necessary
            if neighbor_value < lowest_value:
                lowest_value = neighbor_value
                lowest_value_coords = neighbor_coords

        # If the lowest value is still the current value, break the loop
        if lowest_value == current_value:
            break
        # Otherwise, add the lowest value coordinates to the coords_list
        river_list.append(lowest_value_coords)
        # Update the current coordinates to be the lowest value coordinates
        current_coords = lowest_value_coords
    return river_list

def generate_lake(samples, coords_list):
    lake_bottom = samples[coords_list[-1]]
    lake_start_x, lake_start_y = coords_list[-1]
    lake_height = samples[coords_list[-2]]
    window = np.ones((3, 3), dtype=np.uint8)
    window[1, 1] = 0
    lake_set = set()
    lake_set.add((lake_start_x, lake_start_y))
    lake_set_final = set()

    while True:
        new_lake_set = set()
        for coord in lake_set:
            x, y = coord
            window_start_x = x - 1
            window_start_y = y - 1
            window_end_x = x + 2
            window_end_y = y + 2
            if window_start_x < 0:
                window_start_x = 0
            if window_start_y < 0:
                window_start_y = 0
            if window_end_x >= samples.shape[0]:
                window_end_x = samples.shape[0] - 1
            if window_end_y >= samples.shape[1]:
                window_end_y = samples.shape[1] - 1
            window_region = samples[window_start_x:window_end_x, window_start_y:window_end_y]
            for i in range(window_region.shape[0]):
                for j in range(window_region.shape[1]):
                    if window[i, j] == 1 and window_region[i, j] < lake_height and window_region[i, j] >= lake_bottom:
                        new_coord = (window_start_x + i, window_start_y + j)
                        new_lake_set.add(new_coord)
        if len(new_lake_set) == 0:
            break
        lake_set.update(new_lake_set)
        lake_set = lake_set.difference(lake_set_final)
        # print(f"current lake set: {lake_set}")
        lake_set_final.update(new_lake_set)
        if (lake_start_x, lake_start_y) in lake_set:
            lake_set.remove((lake_start_x, lake_start_y))
    if not len(lake_set_final) == 0:
        return lake_set_final
    else:
        return None


x = 40
y = 20
seed = np.random.randint(0,1001)
# seed = 973
print(f"seed: {seed}")
noise = tcod.noise.Noise(
    dimensions=2,
    algorithm=tcod.noise.Algorithm.PERLIN,
    implementation=tcod.noise.Implementation.FBM,
    hurst=0.5,
    lacunarity=2.0,
    octaves=4.0,
    seed=seed
    )
samples = noise[tcod.noise.grid(shape=(y, x), scale=0.25, origin=(0, 0), indexing="xy")]
samples = (samples + 1.0)

t0 = time.time()
river = generate_river(samples, 0)
print(f"River: {river}")
river2 = generate_river(samples, 1)
print(f"River: {river2}")
river3 = generate_river(samples, 2)
print(f"River: {river3}")
# print(coords_list[-1])
t1 = time.time()
print(f"river gen time:{t1 - t0}")

t0 = time.time()
g = generate_lake(samples, river)
t1 = time.time()
print(g)
print(f"lake gen time:{t1 - t0}")

