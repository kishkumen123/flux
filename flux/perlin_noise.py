import random
import numpy as np
import pyfastnoisesimd as fns
import noise

from flux.fmath import color_lerp, convert_rgb_to_int


class NoiseGenerator:

    def __init__(self, chunk_size, scale, octaves, persistence, lacunarity, offset, colored_height_map):
        self.chunk_size = chunk_size
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.offset = offset
        self.colored_height_map = colored_height_map

    def pgenerate_noise_map(self, coords, seed, shared_terrain):

        def colorize_perlin_points(perlin_value):
            return self.get_perlin_color(perlin_value, self.colored_height_map)

        def grayscale(perlin_value):
            return self.grayscale_noise_point(perlin_value)

        perlin_noise = self.generate_perlin_noise(seed)
        if self.colored_height_map:
            vfunc = np.vectorize(colorize_perlin_points)
        else:
            vfunc = np.vectorize(grayscale)
        noise_map = vfunc(perlin_noise)
        shared_terrain[coords] = noise_map

    def generate_noise_map(self):

        def colorize_perlin_points(perlin_value):
            return self.get_perlin_color(perlin_value, self.colored_height_map)

        perlin_noise = self.generate_perlin_noise()
        vfunc = np.vectorize(colorize_perlin_points)
        noise_map = vfunc(perlin_noise)

        return noise_map

    def grayscale_noise_point(self, perlin_value):
        rgb_color = color_lerp((0, 0, 0), (255, 255, 255), perlin_value)
        int_value = int(convert_rgb_to_int(rgb_color))

        return int_value

    def get_perlin_color(self, height, height_map):
        for item in height_map:
            if height < item[1]:
                int_value = int(convert_rgb_to_int(item[0]))
                return int_value

        return int(convert_rgb_to_int((0, 0, 0)))

    def generate_perlin_noise(self, seed):
        perlin = fns.Noise(seed=seed, numWorkers=6)
        perlin.frequency = self.scale / 1000
        perlin.noiseType = fns.NoiseType.PerlinFractal
        perlin.fractal.octaves = self.octaves
        perlin.fractal.lacunarity = self.lacunarity
        perlin.fractal.gain = self.persistence
        perlin.perturb.perturbType = fns.PerturbType.NoPerturb

        result = perlin.genAsGrid((self.chunk_size, self.chunk_size))
        return result

    def old_generate_perlin_map(self, offset=(0,0)):
        _noise_map = np.ndarray(shape=(self.chunk_size, self.chunk_size), dtype=int)

        if self.scale <= 0:
            self.scale = 1

        random.seed(self.seed)

        octave_offsets = []
        for i in range(round(self.octaves)):
            offset_x = random.randint(-100000, 100000) + offset[0]
            offset_y = random.randint(-100000, 100000) - offset[1]
            octave_offsets.append((offset_x, offset_y))

        half_width = self.chunk_size/2
        half_height = self.chunk_size/2

        for i in range(self.chunk_size):
            for j in range(self.chunk_size):
                amplitude = 1
                frequency = 1
                noise_height = 0

                for o in range(self.octaves ):
                    sample_x = (i-half_width + octave_offsets[o][0])/self.scale * frequency
                    sample_y = (j-half_height + octave_offsets[o][1])/self.scale * frequency

                    perlin_value = noise.pnoise2(sample_x, sample_y)
                    noise_height += perlin_value * amplitude
                    amplitude *= self.persistence
                    frequency *= self.persistence

                _noise_map[i][j] = self.get_perlin_color(noise_height, self.height_map)
                #black and white
                #_noise_map[i][j] = colorize_noise_point(noise_height)

        return _noise_map

    def old_p2generate_noise_map(self, coords, _offset, terrains2):
        perlin_noise = self.old_generate_perlin_map(_offset)
        terrains2[coords] = perlin_noise

