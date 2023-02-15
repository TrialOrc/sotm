import tcod

noise_wavelet_turbulence = tcod.noise.Noise(
    dimensions=2,
    algorithm=tcod.noise.Algorithm.WAVELET,
    implementation=tcod.noise.Implementation.TURBULENCE,
    )

noise_perlin = tcod.noise.Noise(
    dimensions=2,
    algorithm=tcod.noise.Algorithm.PERLIN,
    )

noise_simplex = tcod.noise.Noise(
    dimensions=2,
    algorithm=tcod.noise.Algorithm.SIMPLEX,
    )

noise_simplex_fbm = tcod.noise.Noise(
    dimensions=2,
    algorithm=tcod.noise.Algorithm.SIMPLEX,
    implementation=tcod.noise.Implementation.FBM,
    lacunarity=3.0,
    octaves=1.5,
    )