class Entity():
    def __init__(self):
        self._id = id(self)
        self.components = {}

    def add(self, c, a):
        if c not in self.components.keys():
            self.components[c] = c(**a)
        else:
            raise Exception("cannot add duplicate components: %s to the same entity %s" % (c, self))


class EM():
    entities = {}
    ce_mapping = {}
    components = {}

    @classmethod
    def create(cls, components=None, arguments=None):
        e = Entity()
        EM.entities[e._id] = e

        if components:
            for i, c in enumerate(components):
                if arguments:
                    e.add(c, arguments[i])
                else:
                    e.add(c, {})
                cls.map_components(e, c)
        return e

    @classmethod
    def register_component(cls, c):
        if c.__name__ not in EM.components.keys():
            EM.components[c.__name__] = c
        else:
            raise Exception("components %s already registered" % c.__name__)

    @classmethod
    def map_components(cls, e, c):
        if c not in EM.ce_mapping.keys():
            EM.ce_mapping[c] = []
        EM.ce_mapping[c].append(e)

    @classmethod
    def entities_of_component(cls, *components):
        result = []

        for c in components:
            entities = EM.ce_mapping[c]
            for e in entities:
                if all(c in list(e.components.keys()) for c in components):
                    if e not in result:
                        result.append(e)
        return result

    @classmethod
    def destroy(cls, _id):
        if _id in EM.entities.keys():
            del EM.entities[_id]
        else:
            raise Exception("destroyed e: %s - doesnt exist" % _id)

    @classmethod
    def add(cls, e):
        if not isinstance(e, Entity):
            raise Exception("e: %s - is not an instance of Entity" % e)

        EM.entities[e._id] = e

    @classmethod
    def alive(cls, _id):
        if _id in EM.entities.keys():
            return True
        else:
            return False

    @classmethod
    def flush(cls):
        EM.entities = {}
