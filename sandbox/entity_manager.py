import pygame
import os
import glob
import random
from fmath import v2

from enum import Enum


textures = {}


#class Mappings(Enum): // might be used for faster entity lookups
    #Renderable = "Renderable"

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

    def __repr__(self):
        return "<%s>" % self.__dict__

    def __getattr__(self, attr):
        return None


class EM():
    entities = {}
    #property_map = {} // might be used later for optimized entity lookups

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
    def get(cls, _id):
        return EM.entities.get(_id)

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
            e = None
            with open(_file) as f:
                e = Entity()
                for line in f:
                    if len(line) > 1:
                        if "#noread" in line:
                            e = None
                            break
                        elif "#" in line:
                            continue
                        line = line.strip("\n")
                        line = line.strip(" ")
                        name, value = line.split("=")
                        
                        if e:
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
                            if "#noread" in line or "#" in line:
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
