import torch
import torch.nn as nn
from torchvision import models
class DenseNet(nn.Module):
    def __init__(self):
        super(DenseNet, self).__init__()
        num_classes = 2     #二元分類
        self.model = models.densenet121(pretrained=True) #選用densenet121
        num_features = self.model.classifier.in_features       #取得classfier層的輸入
        self.model.classifier = nn.Linear(num_features, num_classes)    #修改成自己的分類
        self.softmax = nn.Softmax(dim=1)                                #做Softmax
    def forward(self, x):
        output = self.model(x)
        output = self.softmax(output)
        return output