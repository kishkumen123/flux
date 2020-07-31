from pygame.locals import *

class Events:
    events = []

    @classmethod
    def set(cls, _events):
        cls.events += _events

    @classmethod
    def type(cls, _event, _type):
        return _event.type == _type

    @classmethod
    def key(cls, _event, _key, _mod=0, consume=True):
        result =  _event.key == _key and _event.mod == _mod
        if result and consume:
            cls.consume(_event)
        return result

    @classmethod
    def button(cls, _event, _button, consume=True):
        result = _event.button == _button
        if result and consume:
            cls.consume(_event)
        return result

    @classmethod
    def mbutton_down(cls, _button):
        for event in cls.events:
            if cls.type(event, MOUSEBUTTONDOWN):
                #if cls.button(event, _button):
                if event.button == _button:
                    return True
        return False

    @classmethod
    def mbutton_up(cls, _button):
        for event in cls.events:
            if cls.type(event, MOUSEBUTTONUP):
                if event.button == _button:
                #if cls.button(event, _button):
                    return True
        return False

    @classmethod
    def peak(cls, _type):
        for event in cls():
            if event.type == _type:
                return True
        return False

    @classmethod
    def consume(cls, _event):
        cls.events.remove(_event)

    @classmethod
    def clear(cls):
        cls.events = []

    def __new__(cls):
        return cls.events
