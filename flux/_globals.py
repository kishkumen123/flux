from flux.renderer import render_layer, renderer
from collections import OrderedDict


clicked_on_sprites = OrderedDict()
sprite_selection = None
sprite_selection_list = []

running = True
history_output = []
history_input = []
cursor_underscored = 1
editor = 1








# look into these 2
poly_dict = []
rects = []




#
#selection = None
#selection_list = []
#player = None
#
#
#

# this garbage needs to go asap, its being called in main.py to draw everything? or w.e i think its drawing the polygons
def draw_everything():
    for groups in render_layer.values():
        for group in groups.values():
            for renderable in group.values():
                renderer.draw(renderable.type, renderable.data)



# this garbage needs to go asap, its in every ui file
def add_rect(_rect, _color, _layer):
    global rects
    new_rect = Rect(_rect, _color, _layer)
    rects.append(new_rect)
    sorted(rects, key=lambda rect: rect.layer)
#
#
#def set_selection(value):
#    global selection
#    selection = value
#
#
#def get_selection():
#    global selection
#    return selection
#
#
#class Rect:
#
#    def __init__(self, rect, color, layer):
#        self.rect = rect
#        self.color = color
#        self.layer = layer
