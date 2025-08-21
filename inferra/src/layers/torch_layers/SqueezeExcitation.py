import torch
import torch.nn as nn

from inferra.src.layers.torch_layers.layer import TorchLayer
from inferra.src.layers.torch_layers.Swish import Swish


class SqueezeExcitation(TorchLayer):
    def __init__(self, inplanes, se_planes):
        super(SqueezeExcitation, self).__init__()
        self.reduce_expand = nn.Sequential(
            nn.Conv2d(
                inplanes,
                se_planes,
                kernel_size=1,
                stride=1,
                padding=0,
                bias=True,
            ),
            Swish(),
            nn.Conv2d(
                se_planes,
                inplanes,
                kernel_size=1,
                stride=1,
                padding=0,
                bias=True,
            ),
            nn.Sigmoid(),
        )

    def forward(self, x):
        x_se = torch.mean(x, dim=(-2, -1), keepdim=True)
        x_se = self.reduce_expand(x_se)
        return x_se * x
