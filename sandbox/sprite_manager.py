
class SM:

    @classmethod
    def sort_sprites(cls, entities):
        entities.sort(key = lambda x: (x.group, x.layer))
        return entities

    @classmethod
    def sort_ui(cls, canvases):
        canvases.sort(key = lambda x: (x._id))
        return canvases
