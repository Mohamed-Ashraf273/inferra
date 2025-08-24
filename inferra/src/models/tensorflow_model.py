from tensorflow.keras.models import Model


class TensorFlowModel(Model):
    def __init__(self, **kwargs):
        super(TensorFlowModel, self).__init__()

    def forward(self, x):
        raise NotImplementedError(
            "This method is not implemented for this model."
        )
