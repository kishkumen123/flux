import pygame
import os
import glob
import random
from fmath import Vector2

from enum import Enum


textures = {}


class Mappings(Enum):
    Renderable = "Renderable"

class Properties:
    def __init__(self):
        self.Renderable = 0
        self.Movable = 0
        self.MouseMovable = 0
        self.IsParticle = 0

    def __getattr__(self, attr):
        return None

    def __repr__(self):
        return "<%s>" % self.__dict__


class Entity():
    def __init__(self):
        self._id = None
        self.property = Properties()
        self.components = {}

    def __repr__(self):
        return "<%s>" % self.__dict__

    def __getattr__(self, attr):
        return None


class EM():
    entities = {}
   # components = {}
    #property_map = {}

   # @classmethod
   # def create(cls, _id, components=None, arguments=None):
   #     e = Entity()
   #     EM.entities[e._id] = e

   #     if components:
   #         for i, c in enumerate(components):
   #             if arguments:
   #                 e.add(c, arguments[i])
   #             else:
   #                 e.add(c, {})
   #             cls.map_components(e, c)
   #     return e

   # @classmethod
   # def entities_of_property(self, props):
   #     result = EM.property_map.get(props)
   #     return result if result is not None else []
   #     #for e in self.entities.values():

   #     #    for key in props.__dict__.keys():
   #     #        if props.__dict__[key] == e.property.__dict__[key]:
   #     #            result.append(e)

   #     #return result

   # @classmethod
   # def register_component(cls, c):
   #     if c.__name__ not in EM.components.keys():
   #         EM.components[c.__name__] = c
   #     else:
   #         raise Exception("components %s already registered" % c.__name__)

   # @classmethod
   # def map_components(cls, e, c):
   #     if c not in EM.property_map.keys():
   #         EM.property_map[c] = []
   #     EM.property_map[c].append(e._id)

   # @classmethod
   # def entities_of_component(cls, *components):
   #     result = []

   #     for c in components:
   #         entities = EM.property_map.get(c, [])
   #         for e_id in entities:
   #             if all(c in list(EM.entities[e_id].components.keys()) for c in components):
   #                 if e_id not in result:
   #                     result.append(EM.entities[e_id])

   #     return result

   # @classmethod
   # def ids_of_component(cls, *components):
   #     result = []

   #     for c in components:
   #         entities = EM.property_map.get(c, [])
   #         for e_id in entities:
   #             if all(c in list(EM.entities[e_id].components.keys()) for c in components):
   #                 if e_id not in result:
   #                     result.append(e_id)

   #     return result

    @classmethod
    def destroy(cls, e_id):
        if e_id in EM.entities.keys():
            del EM.entities[e_id]
            #for key in EM.property_map.keys():
                #if e_id in EM.property_map[key]:
                    #EM.property_map[key].remove(e_id)
        else:
            raise Exception("cant destroy e: %s - doesnt exist" % _id)

    @classmethod
    def add(cls, e):
        if not isinstance(e, Entity):
            raise Exception("e: %s - is not an instance of Entity" % e)

        EM.entities[e._id] = e
        #for key in e.property.__dict__.keys():
            #EM.property_map[key] = e

    @classmethod
    def alive(cls, e_id):
        return e_id in EM.entities.keys()

    @classmethod
    def flush(cls):
        EM.entities = {}

    @classmethod
    def load_entities(cls, path):
        files = glob.glob(path)
        for _file in files:
            with open(_file) as f:
                e = Entity()
                for line in f:
                    if len(line) > 1:
                        if "#noread" in line:
                            e = None
                            break
                        line = line.strip("\n")
                        line = line.strip(" ")
                        name, value = line.split("=")
                        
                        e.__dict__[name] = eval(value)
                        if name in e.property.__dict__.keys():
                            e.property.__dict__[name] = eval(value)
                            
            if e: 
                if e._id is None:
                    e.__dict__["_id"] = eval(os.path.basename(_file).split("_")[-1])
                EM.add(e)

    @classmethod
    def load_entity(cls, entity):
        files = glob.glob("data/entities/*")
        for _file in files:
            if entity in _file:
                with open(_file) as f:
                    e = Entity()
                    for line in f:
                        if len(line) > 1:
                            if "#noread" in line:
                                continue
                            line = line.strip("\n")
                            line = line.strip(" ")
                            name, value = line.split("=")
                            
                            e.__dict__[name] = eval(value)
                            if name in e.property.__dict__.keys():
                                e.property.__dict__[name] = eval(value)
                                
                if e._id is None:
                    e.__dict__["_id"] = eval(os.path.basename(_file).split("_")[-1])
                EM.add(e)





def load_textures(path):
    files = glob.glob(path)
    for _file in files:
        textures[os.path.basename(_file)] = pygame.image.load(_file)
