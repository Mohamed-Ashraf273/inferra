import torch.nn as nn


class TorchLayer(nn.Module):
    def __init__(self):
        super(TorchLayer, self).__init__()
        self.layer_name = None

    def forward(self, x):
        raise NotImplementedError(
            "This method should be overridden by {}".format(self.layer_name)
        )
