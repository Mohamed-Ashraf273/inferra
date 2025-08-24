import torch.nn as nn

from inferra.src.layers.torch_layers.ResidualBlock import ResidualBlock


class Au57(nn.Module):
    """
    Au57: A deep convolutional neural network model
    based on residual blocks.

    This model is designed for classification tasks and consists of:
    - An initial convolutional layer with batch normalization
      and ReLU activation.
    - Four residual layers (res_layer1 to res_layer4)
      composed of ResidualBlock modules.
    - Adaptive average pooling to reduce feature maps to 1x1 spatial size.
    - Flattening, dropout, and a fully connected layer
      to produce class logits.

    Architecture:
    -------------
    Input: single-channel image/tensor (e.g., spectrogram)
    of shape [batch_size, 1, height, width]
    conv1 -> res_layer1 -> res_layer2 -> res_layer3 -> res_layer4
    -> avg_pool -> flatten -> dropout -> fc (num_classes output)

    Parameters:
    -----------
    num_classes : int, default=50
        Number of output classes for the final fully connected layer.

    Notes:
    ------
    - The model expects **1 input channel**.
      If your input has multiple channels,
      you must convert or preprocess it to a
      single-channel format.
    - ResidualBlock modules are used for all
      residual layers to allow deeper architectures
      without vanishing gradient issues.

    Methods:
    --------
    forward(x)
        Defines the forward pass of the network.
        x : torch.Tensor
            Input tensor of shape [batch_size, 1, height, width]
        Returns:
            torch.Tensor of shape [batch_size, num_classes]
            containing raw class scores (logits).

    Example:
    --------
    >>> model = Au57(num_classes=10)
    >>> input_tensor = torch.randn(8, 1, 128, 128)
    >>> output = model(input_tensor)
    >>> output.shape
    torch.Size([8, 10])
    """

    def __init__(self, num_classes=50):
        super(Au57, self).__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(
                in_channels=1,
                out_channels=64,
                kernel_size=7,
                stride=2,
                padding=3,
                bias=False,
            ),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
        )
        self.res_layer1 = nn.ModuleList(
            [ResidualBlock(in_channels=64, out_channels=64) for _ in range(3)]
        )
        self.res_layer2 = nn.ModuleList(
            [
                ResidualBlock(
                    in_channels=64 if i == 0 else 128,
                    out_channels=128,
                    stride=2 if i == 0 else 1,
                )
                for i in range(4)
            ]
        )
        self.res_layer3 = nn.ModuleList(
            [
                ResidualBlock(
                    in_channels=128 if i == 0 else 256,
                    out_channels=256,
                    stride=2 if i == 0 else 1,
                )
                for i in range(6)
            ]
        )
        self.res_layer4 = nn.ModuleList(
            [
                ResidualBlock(
                    in_channels=256 if i == 0 else 512,
                    out_channels=512,
                    stride=2 if i == 0 else 1,
                )
                for i in range(3)
            ]
        )
        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.flatten = nn.Flatten()
        self.dropout = nn.Dropout(0.5)
        self.fc = nn.Linear(in_features=512, out_features=num_classes)

    def forward(self, x):
        x = self.conv1(x)
        for block in self.res_layer1:
            x = block(x)
        for block in self.res_layer2:
            x = block(x)
        for block in self.res_layer3:
            x = block(x)
        for block in self.res_layer4:
            x = block(x)
        x = self.avg_pool(x)
        x = self.flatten(x)
        x = self.dropout(x)
        x = self.fc(x)
        return x
