from model.my_model import DenseNet
import torch
from glob import glob
from model.dataprocessing.dataprocessing import *
import warnings
import sys
from model.trim_wav_file import trim_audio

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

warnings.filterwarnings("ignore")

def model_test(datas,labels,weights):
    net = DenseNet()
    net.load_state_dict(torch.load(weights))
    net.eval()
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
    return acc, total

def model_test_single(file,weights):       # 丟入wav檔案
    net = DenseNet().to(device)
    net.load_state_dict(torch.load(weights))
    net.eval()
    single = get_files(file)[0]
    input = create_single_data(single)
    input = torch.from_numpy(input)
    input = input.to(device)
    input = input.unsqueeze(0)
    output = net(input)
    return output

def return_to_web(a,b):
    if a > b:
        return 0 
    else:
        return 1
    
def main(input):
    output_wav = './store5.wav'
    print(output_wav)
    trim_audio(input,output_wav)       #切5秒影片
    out = model_test_single(output_wav,'./model/model_para4.pth')
    print(out)
    return_value = return_to_web(out[0][0],out[0][1])
    print(return_value)
    return return_value
    
if __name__=='__main__':
    if len(sys.argv) != 2:
        print("Usage: python use_model.py <path_to_wav_file>")
        sys.exit(1)
    input = sys.argv[1]
    output_wav = './store5.wav'
    trim_audio(input,output_wav)       #切5秒影片
    out = model_test_single(output_wav,'./model_para4.pth')
    print(out)
    return_value = return_to_web(out[0][0],out[0][1])
    print(return_value)
    