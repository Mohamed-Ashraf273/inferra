from inferra.src.layers.torch_layers.layer import TorchLayer


class Flatten(TorchLayer):
    def forward(self, x):
        return x.reshape(x.shape[0], -1)
