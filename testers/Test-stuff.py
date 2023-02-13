import matplotlib.pylab as plt
import numpy as np
from tcod import noise
import time

x = np.linspace(np.pi, -np.pi, 24) # Create 24 evenly spaced numbers between pi and -pi.
y = np.sin(x) #  Return the sin of x, creates a sine wave
pos_sin = np.sin(-x)[6:-6]
neg_sin = np.sin(x)[6:-6]

pos_sin_static = np.array([1., 0.94226092, 0.81696989, 0.63108794, 0.39840109, 0.13616665,
                    -0.13616665, -0.39840109, -0.63108794, -0.81696989, -0.94226092, -1.])
neg_sin_static = np.array([-1., -0.94226092, -0.81696989, -0.63108794, -0.39840109, -0.13616665,
                    0.13616665, 0.39840109, 0.63108794, 0.81696989, 0.94226092, 1.])

np_noise = np.random.normal(0, 0.1, 100) #  Create gausian noise. Mean of 0, 0.1 distribution, 100 samples (1d).
tcod_noise = noise.Noise(dimensions=1, algorithm=noise.Algorithm.SIMPLEX, implementation=noise.Implementation.SIMPLE)

'''
for i in range(len(y)):
    #  Add noise to Sine wave
    y[i] = y[i] + np_noise[i]
'''

class Weather:
    'class to hold all weather functions.'
    x = np.linspace(np.pi, -np.pi, 24) # Create 24 evenly spaced numbers between pi and -pi.
    pos_sin = np.sin(x)[6:-6]
    neg_sin = np.sin(-x)[6:-6]
    def __init__(self) -> None:
        self.max_hi = 272  # Temp in Kelvin, appx 30 F
        self.max_lo = 239  # Temp in Kelvin, appx -30 F

    def generate_hi_lo(self):
        range = int(round((np.mean(np.random.random(2)) * 11) + 2))
        lo = np.random.randint(self.max_lo, (self.max_hi - range + 1), 3)
        weighted_lo = np.mean(lo)
        hi = weighted_lo + range
        return int(weighted_lo), int(hi)

    def temp_gradient(self, weathers: list):
        weathers = weathers.ravel()
        temps = np.empty((len(weathers), 12))
        for x in range(len(weathers) - 1):
            if weathers[x] < weathers[x + 1]:
                positive_array = ((self.pos_sin + 1) * ((weathers[x + 1] - weathers[x]) / 2)) + weathers[x]
                temps[x] = (positive_array[::-1])
            elif weathers[x] >= weathers[x + 1]:
                neg_list = ((self.neg_sin + 1) * ((weathers[x] - weathers[x + 1]) / 2)) + weathers[x + 1]
                temps[x] = (neg_list[::-1])
        if weathers[-1] >= weathers[0]:
            pos_array = ((self.pos_sin + 1) * ((weathers[-1] - weathers[0]) / 2)) + weathers[0]
            temps[-1] = (pos_array)
        elif weathers[-1] < weathers[0]:
            neg_array = ((self.neg_sin + 1) * ((weathers[0] - weathers[-1]) / 2)) + weathers[-1]
            temps[-1] = (neg_array)


        temps = np.around(temps, 1)
        # temp_list = temp_list.astype(int)        
        # temp_list = [num for elem in temp_list for num in elem]
        return temps.ravel()

t0 = time.time()
iters = 2000
warray = np.empty((iters, 2))
w = Weather()
# warray = np.repeat((w.generate_hi_lo()), iters)

for x in range(iters):
    wx, wy = w.generate_hi_lo()
    warray[x] = (wx, wy)

# print(warray)
t1 = time.time()
weather_scroll = w.temp_gradient(warray)
t2 = time.time()
print(len(weather_scroll))
print(t1 - t0)
print(t2 - t1)
print(weather_scroll.max())
print(weather_scroll.min())
# print(weather_scroll)
#  Used for testing:
graph_x = np.linspace(0, len(weather_scroll), len(weather_scroll))

plt.plot(graph_x, weather_scroll)
plt.xlabel('Hours')
plt.ylabel('Temperature')
plt.axis('tight')
plt.ylim(239, 272)
plt.show()

