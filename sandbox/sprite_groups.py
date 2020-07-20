import pygame

class Sprite(pygame.sprite.Sprite):

    def __init__(self, image="", group="", layer=0):

        self.name = image.split(".")[0]
        #TODO: need to call .convert() pygame.image.load() but its removing the transparency for w.e reason 
        self.image = pygame.image.load(image)
        #self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self._layer = layer
        pygame.sprite.Sprite.__init__(self, sprite_groups.get_group(group))

    def __repr__(self):
        return "<Sprite - name: %s, layer: %s>" % (self.name, self._layer)

    def __str__(self):
        return "<Sprite - name: %s, layer: %s>" % (self.name, self._layer)

class SpriteGroups():

    def __init__(self):
        self.group_dict = {}

    def get_group(self, name):
        return self.group_dict[name]

    def create(self, name):
        self.group_dict[name] = pygame.sprite.LayeredUpdates()

    def flush(self):
        self.group_dict = {}

sprite_groups = SpriteGroups()

