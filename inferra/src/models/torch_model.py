import torch.nn as nn


class TorchModel(nn.Module):
    def __init__(self):
        super(TorchModel, self).__init__()
        self.model_name = "BaseModel"
        self.model_type = "Generic"

    def preprocess(self, data):
        raise NotImplementedError(
            "This method should be overridden by {}".format(self.model_name)
        )

    def run_inference(self, test_data):
        raise NotImplementedError(
            "This method should be overridden by {}".format(self.model_name)
        )

    def summary(self):
        raise NotImplementedError(
            "This method should be overridden by {}".format(self.model_name)
        )

    def get_load_weights(self, filepath):
        raise NotImplementedError(
            "This method should be overridden by {}".format(self.model_name)
        )
