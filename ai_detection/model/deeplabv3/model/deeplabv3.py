#deeplabv3网络

import torch.nn as nn
import torch.nn.functional as F
from .resnet import ResNet18_OS8
from .aspp import ASPP

class DeepLabV3(nn.Module):
    def __init__(self):
        super(DeepLabV3, self).__init__()

        self.num_classes = 16

        self.resnet = ResNet18_OS8()
        self.aspp = ASPP(num_classes=self.num_classes)

    def forward(self, x):
        # (x has shape (batch_size, 3, h, w))

        h = x.size()[2]
        w = x.size()[3]

        feature_map = self.resnet(x) # (shape: (batch_size, 512, h/16, w/16)) (assuming self.resnet is ResNet18_OS16 or ResNet34_OS16. If self.resnet is ResNet18_OS8 or ResNet34_OS8, it will be (batch_size, 512, h/8, w/8). If self.resnet is ResNet50-152, it will be (batch_size, 4*512, h/16, w/16))

        output = self.aspp(feature_map) # (shape: (batch_size, num_classes, h/16, w/16))

        output = F.upsample(output, size=(h, w), mode="bilinear") # (shape: (batch_size, num_classes, h, w))

        return output

