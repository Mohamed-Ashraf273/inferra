from tensorflow.keras.layers import Layer


class TensorFlowLayer(Layer):
    def __init__(self):
        super(TensorFlowLayer, self).__init__()
        self.layer_name = None

    def forward(self, x):
        raise NotImplementedError(
            "This method should be overridden by {}".format(self.layer_name)
        )
