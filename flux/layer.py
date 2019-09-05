

class Layer:
    layer = "layer_0"
    layer_list = ["layer_0"]

    @classmethod
    def set_layer(cls, layer):
        if layer in cls.layer_list:
            return "FUCK OFF IM ALREADY IN HERE"

        cls.layer_list.append(layer)
        cls.layer = layer

    @classmethod
    def pop_layer(cls):
        cls.layer_list.pop()
        cls.layer = cls.layer_list[-1]

    @classmethod
    def get_layer(cls):
        return cls.layer

