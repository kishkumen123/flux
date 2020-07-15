class Layer:

    def __init__(self):
        self.layer = "layer_0"
        self.layer_list = ["layer_0"]

    def append(self, layer):
        if layer not in self.layer_list:
            self.layer_list.append(layer)
            self.layer = layer

    def set_layer(self, layer):
        if layer in self.layer_list:
            return

        self.layer_list.append(layer)
        self.layer = layer

    def pop_layer(self):
        self.layer_list.pop()
        self.layer = self.layer_list[-1]

    def get_layer(self):
        return self.layer

    def current_layer_is(self, layer_name):
        if layer_name == 'layer_all' or layer_name == layer.get_layer():
            return True
        return False


layer = Layer()
