import segmentation_models_pytorch as smp
import torch.nn as nn

class DeepLabModel(nn.Module):

    def __init__(self, num_classes=7):

        super().__init__()

        self.model = smp.DeepLabV3Plus(

            encoder_name="resnet34",
            encoder_weights="imagenet",

            in_channels=3,

            classes=num_classes,

            activation=None

        )

    def forward(self, x):

        return self.model(x)