from typing import Any

import numpy as np
import time
import scipy.signal  # type: ignore
from numpy.typing import NDArray

death_limit = 3
birth_limit = 4
map_collection = []

def initialize_ca(map_width, map_height):

    CA_map = np.where(
        np.random.rand(map_height, map_width).T > 0.45,
        0,
        1,
    )

    return CA_map

def count_alive(map, x, y):
    height = len(map)
    width = len(map[0])
    alive_count = 0
    # for (x, y), i in np.ndenumerate(map):
    for i in range(-1, 2):
        for j in range(-1, 2):
            neighbor_x = x + i
            neighbor_y = y + j
            if i == 0 and j == 0:
                continue
            elif neighbor_x < 0 or neighbor_y < 0 or neighbor_y >= height or neighbor_x >= width:
                alive_count += 1
            elif map[neighbor_x][neighbor_y] == 1:
                alive_count += 1

    return alive_count
            

def step_ca(map, steps):
    for step in range(steps):
        for (x, y), i in np.ndenumerate(map):
            #  Use NumPy ndenumerate to iterate through the game map.
            #  (x, y) are coordinates, i is the value of the tile.
            alive = count_alive(map, x, y) #  Each time we will check values around our tile.
            if i == 1: #  If the tile is 'alive'
                if alive < death_limit: #  Check it against the death limit
                    map[x, y] = 0
                    # i = 0 # If not enough living neighbors, kill it.
            elif i == 0: # If the tile is 'dead'
                if alive > birth_limit:
                    map[x][y] = 1
                    # i = 1
        # print(map)
        # step + 1
        # map_collection.append(map)
    return map

def convolve(tiles: NDArray[Any], wall_rule: int = 5) -> NDArray[np.bool_]:
    neighbors: NDArray[Any] = scipy.signal.convolve2d(tiles == 0, [[1, 1, 1],[1, 1, 1],[1, 1, 1]], "same")
    next_tiles: NDArray[np.bool_] = neighbors < wall_rule
    return next_tiles

def show(tiles:NDArray[Any]) -> None:
    for line in tiles:
        print("".join("# "[int(cell)] for cell in line))


w = 20
h = 20
'''
start = time.time()
test_map=initialize_ca(w,h)
# print(test_map)
test_map2=step_ca(test_map, 4)
# print(test_map2)

if np.array_equal(test_map, test_map2) is True:
    print('fail')

arr = np.zeros((3, 3))

steps = 4

for step in range(steps):
    for (x, y), i in np.ndenumerate(arr):
        if i == 0:
            arr[x, y] = 1

print(arr)
'''
t0 = time.time()
test_arr = initialize_ca(10, 10)
test_arr = step_ca(test_arr, 4)
t1 = time.time()
print(t1 - t0)

t2 = time.time()
w, h = 25, 25
convolve_test = initialize_ca(w, h)
for _ in range(4):
    convolve_test = convolve(convolve_test)
t4 = time.time()
add_rand_tress = np.where(
        np.random.rand(h, w).T > 0.9,
        True,
        False,
    )
remove_rand_tress = np.where(
        np.random.rand(h, w).T > 0.9,
        True,
        False,
    )    
convolve_test = np.logical_or(convolve_test, add_rand_tress)
convolve_test = np.logical_and(convolve_test, np.logical_not(remove_rand_tress))
t3 = time.time()
print(f"initial gen:{t4 - t2}")
print(f"add trees gen:{t3 - t4}")
show(convolve_test)