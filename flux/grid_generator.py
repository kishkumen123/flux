import pygame
from multiprocessing import Process, Manager

from flux.screen import Display
from flux.terrain import Terrain
from flux.perlin_noise import NoiseGenerator
from flux.fmath import v2distance


class GridGenerator:

    def __init__(self, view_distance, chunk_size, scale, octaves, persistence, lacunarity, seed, offset, color_height_map):
        self.chunk_size = chunk_size
        self.view_distance = view_distance
        self.chunks_visable_in_view_distance = (int(view_distance / chunk_size))
        self.scale = scale
        self.octaves = octaves
        self.persistence = persistence
        self.lacunarity = lacunarity
        self.seed = seed
        self.offset = offset
        self.color_height_map = color_height_map
        self.terrains = {}
        self.process_shared_terrains = Manager().dict()
        self.grid_position = [Display.fake_display.get_width()/2, Display.fake_display.get_height()/2]
        self.noise_generator = NoiseGenerator(self.chunk_size, self.scale, self.octaves, self.persistence, self.lacunarity, (0, 0), self.color_height_map)

    def move(self, x=0, y=0):
        self.grid_position[0] += x
        self.grid_position[1] += y

    def update(self):
        current_chunk_coord_x = round(self.grid_position[0] / self.chunk_size)
        current_chunk_coord_y = round(self.grid_position[1] / self.chunk_size)

        for y in range(-self.chunks_visable_in_view_distance, self.chunks_visable_in_view_distance):
            for x in range(-self.chunks_visable_in_view_distance, self.chunks_visable_in_view_distance):
                viewed_chunk_coord = (current_chunk_coord_x + x, current_chunk_coord_y + y)

                if str(viewed_chunk_coord) not in self.terrains.keys():
                    self.seed += 1
                    self.terrains[str(viewed_chunk_coord)] = Terrain(self.chunk_size, viewed_chunk_coord[0], viewed_chunk_coord[1], self.seed)
                    process = Process(target=self.noise_generator.pgenerate_noise_map, args=(str(viewed_chunk_coord), self.seed, self.process_shared_terrains))
                    process.start()

        for key, noise_map in self.process_shared_terrains.items():
            pygame.pixelcopy.array_to_surface(self.terrains[key].surface, noise_map)
            del self.process_shared_terrains[key]

        for value in self.terrains.values():
            if v2distance(self.grid_position, (value.xposition, value.yposition)) < self.view_distance and value.surface is not None:
                Display.fake_display.blit(value.surface, (value.xposition + (-self.grid_position[0]), value.yposition + (-self.grid_position[1])))

