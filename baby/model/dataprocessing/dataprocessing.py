import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from glob import glob
import librosa
import librosa.display
import torchvision
from PIL import Image

#
def get_files(files_path):                  #
    audio_files = glob(files_path)
    return audio_files

def  turn_files_into_data(audio_files):         #
    y_list=[]
    sr_list=[]
    for audio_file in audio_files:
        y_list.append(librosa.load(audio_file)[0])   #音檔相對振幅
        sr_list.append(librosa.load(audio_file)[1])  #sample_rate 採樣頻率
    return y_list, sr_list

def trim_data(datas, sample_rate, time):
    sr = sample_rate
    target_length = time * sr #目標音檔長度
    y_trimmed_list = []
    for data in datas:
        y_trimmed, _ = librosa.effects.trim(data,top_db=60)        #設定閾值80 
        if len(y_trimmed)>target_length:
            y_trimmed =  y_trimmed[:target_length]
        y_trimmed_list.append(y_trimmed)
    return y_trimmed_list

def build_3_channels_melspectrograms(data,sample_rate):     #製作3通道梅爾頻譜圖
    num_channels = 3 
    #設定三個不同窗口和跳躍距離
    hop_size = [128,256,512]
    win_size = [100,200,400]
    #轉換成梅爾頻譜圖
    S_db_channels = []
    for j in range(num_channels):
        S = librosa.feature.melspectrogram(y=data,      
                                           sr=sample_rate,
                                           hop_length = hop_size[j],
                                           win_length=win_size[j]
                                           )
        S_db_mel = librosa.amplitude_to_db(S,ref=np.max)    #把音檔從振幅轉成分貝
        S_db_mel = np.asarray(torchvision.transforms.Resize((224, 224))(Image.fromarray(S_db_mel))) #把圖片轉成224*224可輸入pretrained model
        S_db_channels.append(S_db_mel)                          
    S_db_channels_arr = np.array(S_db_channels)
    return S_db_channels_arr

def create_dataset_with_label(data,label):
    new_entry = {}
    new_entry['values'] = data
    new_entry['target'] = label
    return new_entry

def create_with_trimmed(path,sample_rate=22050,label=1):
    files = get_files(path)
    y, sr = turn_files_into_data(files)
    trimmed_data = trim_data(y,sample_rate=sample_rate,time=5)
    imgs = []
    for data in trimmed_data:
        img = build_3_channels_melspectrograms(data,sample_rate=sample_rate)
        imgs.append(img)
    dataset = []
    for img in imgs:
        dataset.append(create_dataset_with_label(img,label))
    return dataset

def create_with_no_trimmed(path,sample_rate=22050,label=1):
    files = get_files(path)
    y, sr = turn_files_into_data(files)
    imgs = []
    for data in y:
        img = build_3_channels_melspectrograms(data,sample_rate=sample_rate)
        imgs.append(img)
    dataset = []
    for img in imgs:
        dataset.append(create_dataset_with_label(img,label))
    return dataset

def create_single_data(data,sample_rate=22050):       #單一資料input
    y = librosa.load(data)[0]   #音檔相對振幅
    sr = librosa.load(data)[1] #sample_rate 採樣頻率
    num_channels = 3 
    #設定三個不同窗口和跳躍距離
    hop_size = [128,256,512]
    win_size = [100,200,400]
    #轉換成梅爾頻譜圖
    S_db_channels = []
    for j in range(num_channels):
        S = librosa.feature.melspectrogram(y=y,      
                                           sr=sample_rate,
                                           hop_length = hop_size[j],
                                           win_length=win_size[j]
                                           )
        S_db_mel = librosa.amplitude_to_db(S,ref=np.max)    #把音檔從振幅轉成分貝
        S_db_mel = np.asarray(torchvision.transforms.Resize((224, 224))(Image.fromarray(S_db_mel))) #把圖片轉成224*224可輸入pretrained model
        S_db_channels.append(S_db_mel)                          
    S_db_channels_arr = np.array(S_db_channels)
    return S_db_channels_arr
