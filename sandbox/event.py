

class Event:
    events = []
    mapping = {}
    

    @classmethod
    def set(cls, _events):
        Event.events = _events

    @classmethod
    def get(cls):
        return Event.events

    @classmethod
    def isof(cls, _event, _type):
        if _event.type == _type:
            i = Event.events.index(_event)
            Event.events.pop(i)
            return True
        return False
