
class SM:

    @classmethod
    def sort(cls, entities):
        entities.sort(key = lambda x: (x.group, x.layer))
        return entities

