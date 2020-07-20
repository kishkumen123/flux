#from entity_manager import EM
from components import Sprite

class SM:

    @classmethod
    def sort(cls, entities):
        result = []

        entities.sort(key = lambda x: (x.components[Sprite].group, x.components[Sprite].layer))
        return entities


#EM.register_component(Sprite)
#
#EM.create([Sprite], [{"image": "", "group": 3, "layer": 0}])
#EM.create([Sprite], [{"image": "", "group": 3, "layer": 1}])
#EM.create([Sprite], [{"image": "", "group": 3, "layer": 2}])
#EM.create([Sprite], [{"image": "", "group": 6, "layer": 2}])
#EM.create([Sprite], [{"image": "", "group": 6, "layer": 1}])
#EM.create([Sprite], [{"image": "", "group": 6, "layer": 0}])
#EM.create([Sprite], [{"image": "", "group": 2, "layer": 1}])
#EM.create([Sprite], [{"image": "", "group": 2, "layer": 0}])
#EM.create([Sprite], [{"image": "", "group": 2, "layer": 2}])
#
#
#
#
#entities = EM.entities_of_component(Sprite)
#
#for e in entities:
#    sprite = e.components[Sprite]
#    print("%s - %s" % (sprite.group, sprite.layer))
#
#print("---------------")
#result = SM.sort(entities)
#for e in result:
#    sprite = e.components[Sprite]
#    print("%s - %s" % (sprite.group, sprite.layer))
