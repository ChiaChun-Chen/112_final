from torch.utils.data import Dataset

class AudioDataset(Dataset):
    def __init__(self, features, targets):  #輸入切分數據集的特徵和標籤
        self.features = features
        self.targets = targets

    def __len__(self):
        return len(self.features)   #返回資料集長度

    def __getitem__(self, idx):     #返回梅爾頻譜圖和標籤
        feature = self.features[idx]
        target = self.targets[idx]
        return feature, target

