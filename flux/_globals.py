from flux.renderer import RenderLayer, renderer

running = True
history_output = []
history_input = []
cursor_underscored = 1
editor = 1
poly_dict = []
selection = None
selection_list = []
player = None

rects = []

render_layer = RenderLayer()
render_layer.create_layer()


def draw_everything():
    for groups in render_layer.values():
        for group in groups.values():
            for item in group.values():
                renderer.draw(item["type"], item["data"])


def add_rect(_rect, _color, _layer):
    global rects
    new_rect = Rect(_rect, _color, _layer)
    rects.append(new_rect)
    sorted(rects, key=lambda rect: rect.layer)


def set_selection(value):
    global selection
    selection = value


def get_selection():
    global selection
    return selection


class Rect:
    def __init__(self, rect, color, layer):
        self.rect = rect
        self.color = color
        self.layer = layer
