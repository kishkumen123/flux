

class UILayer:

    def __init__(self):
        self.layer = "layer_0"
        self.layer_list = ["layer_0"]

    def set_layer(self, layer):
        if layer in self.layer_list:
            return "FUCK OFF IM ALREADY IN HERE"

        self.layer_list.append(layer)
        self.layer = layer

    def pop_layer(self):
        self.layer_list.pop()
        self.layer = self.layer_list[-1]

    def get_layer(self):
        return self.layer


class RenderLayer:

    def __init__(self):
        self.layer = "layer_0"
        self.layer_list = ["layer_0"]

    def set_layer(self, layer):
        if layer in self.layer_list:
            return "FUCK OFF IM ALREADY IN HERE"

        self.layer_list.append(layer)
        self.layer = layer

    def pop_layer(self):
        self.layer_list.pop()
        self.layer = self.layer_list[-1]

    def get_layer(self):
        return self.layer


render_layer = RenderLayer()
layer = UILayer()
