
import numpy as np
import matplotlib.pylab as plt
import torch
import torchvision
from PIL import Image
from dataprocessing.dataprocessing import *
from sklearn.model_selection import train_test_split 
from torch.utils.data import Dataset, DataLoader
from Audiodataset import AudioDataset
from my_model import DenseNet
import torch.optim as optim
import torch.nn as nn
from tqdm import tqdm
from test_model import model_test

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
cry_path = './data/*/*/*.wav'   #label 1
ECS_path = './audio/*.wav'      #label 0
people_speak_path = './people_speak_wav/*.wav'  #label 0 
music_path = './'
PATH = './model_saved.pth'           #模型存檔
sample_rate = 22050
cry_dataset = create_with_trimmed(cry_path,label=1)                           #製作哭聲數據集 label1
no_cry_dataset = create_with_no_trimmed(ECS_path,label=0)               #環境數據集     label0
people_speak_dataset = create_with_trimmed(people_speak_path,label=0)          #label0
dataset = cry_dataset + no_cry_dataset + people_speak_dataset
print(len(dataset),len(cry_dataset))
featureset =[entry['values'] for entry in dataset]
targetset = [entry['target'] for entry in dataset]
X_train, X_test, Y_train, Y_test = train_test_split(featureset,targetset,test_size=0.2,random_state=42)

trainset = AudioDataset(X_train,Y_train)
testset = AudioDataset(X_test,Y_test) 
train_Loader = DataLoader(trainset,batch_size=8,shuffle=True,num_workers=4)
test_Loader = DataLoader(testset,batch_size=4,shuffle=False,num_workers=4)
criterion = nn.CrossEntropyLoss()               #loss function
net = DenseNet().to(device)
optimizer= optim.SGD(net.parameters(),lr=0.0001,momentum=0.9)  #設定優化方法(提供模型參數、學習率、momentum幫助沖出local minimum)

def train_model(model,dataloader,lossfn,optimizer):  #模型訓練
    epochs = 80
    model.train()
    for epoch in range(epochs):        #跑epoch
        running_loss = 0.0      #紀錄loss
        with tqdm(total=len(dataloader)) as t:  #做進度條
                
            for i, data in enumerate(train_Loader, 0):      #enumerate用於將一個可遍歷的數列作編號，0表示從0開始編
                # get the inputs; data is a list of [inputs, labels]
                inputs, labels = data
                inputs = inputs.to(device)
                labels =labels.to(device)
                # zero the parameter gradients 讓梯度先歸零，才能作下次計算
                optimizer.zero_grad()

                # forward + backward + optimize
                outputs = model(inputs)
                loss = lossfn(outputs, labels)
                loss.backward()
                optimizer.step()
                t.update()
                # print statistics
                running_loss += loss.item() ##加上損失函數
                if i % 200 == 199:    # print every 200 mini-batches
                    print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 200:.3f}')
                    running_loss = 0.0
    model.eval()
    print('Finished Training')

train_model(net,train_Loader,criterion,optimizer=optimizer)
torch.save(net.state_dict(), PATH)
print(PATH)
print('model is saved')

acc = 0
total = 0
dataiter = iter(test_Loader)
for images, labels in dataiter:
    acc_count, total_count = model_test(images, labels=labels, weights=PATH)
    acc += acc_count
    total += total_count

print(acc/total)