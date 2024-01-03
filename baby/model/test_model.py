from model.my_model import DenseNet
import torch
from glob import glob
from model.dataprocessing.dataprocessing import *
import warnings
import sys
warnings.filterwarnings("ignore")

def model_test(datas,labels,weights):
    net = DenseNet()
    net.load_state_dict(torch.load(weights))
    outputs = net(datas)
    k=[]
    acc = 0.
    total = 0.
    for output in outputs:
        if output[0]>output[1]:
            k .append(0)
        else:
            k.append(1)
    for i in range(len(labels)):
        if k[i] == labels[i].item():
            acc+=1
        total+=1
    accuracy = acc/total
    print('accuracy: ',acc/total)
    return accuracy

def model_test_single(file,weights):       # 丟入wav檔案
    net = DenseNet()
    net.load_state_dict(torch.load(weights))
    single = get_files(file)[0]
    single = file
    input = create_single_data(single)
    input = torch.from_numpy(input).float()
    input = input.unsqueeze(0)
    output = net(input)
    return output

if __name__=='__main__':
    if len(sys.argv) != 2:
        print("Usage: python use_model.py <path_to_wav_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    out = model_test_single(input_file,'./densenet.pth')
    if out[0][0]>out[0][1]:
        print(0)
    else:
        print(1)