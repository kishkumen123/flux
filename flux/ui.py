from ui_panel import Panel
from ui_button import Button
from ui_slider import Slider


class UI:

    def __init__(self):
        self.panels = {}

    def create_panel(self, name, **kwargs):
        if kwargs.get("size") is None:
            kwargs["size"] = [50, 100]
        if kwargs.get("position") is None:
            kwargs["position"] = [0, 0]

        self.panels[name] = Panel(name, **kwargs)

    def create_button(self, name, parent, **kwargs):
        if kwargs.get("size") is None:
            kwargs["size"] = [50, 100]
        if kwargs.get("position") is None:
            kwargs["position"] = [0, 0]

        panel = self.panels[parent]
        panel.attach(Button(name, parent, panel.position, **kwargs))

    def create_slider(self, name, parent, sl_range, **kwargs):
        if kwargs.get("size") is None:
            kwargs["size"] = [50, 100]
        if kwargs.get("position") is None:
            kwargs["position"] = [0, 0]

        panel = self.panels[parent]
        panel.attach(Slider(name, parent, panel.position, sl_range, **kwargs))

    def show_panel(self, name):
        self.panels[name].show = True

    def toggle_panel(self, name):
        self.panels[name].show = not self.panels[name].show

    def update(self):
        for panel in self.panels.values():
            if panel.show:
                panel.draw()
                panel.update()


ui = UI()

