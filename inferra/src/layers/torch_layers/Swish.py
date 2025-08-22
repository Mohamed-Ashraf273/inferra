import torch

from inferra.src.layers.torch_layers.layer import TorchLayer


class Swish(TorchLayer):
    def __init__(self):
        super(Swish, self).__init__()

    def forward(self, x):
        return x * torch.sigmoid(x)
