import random 

ServerURL = 'https://class.iottalk.tw' #For example: 'https://iottalk.tw'
MQTT_broker = 'class.iottalk.tw' # MQTT Broker address, for example:  'iottalk.tw' or None = no MQTT support
MQTT_port = 5566
MQTT_encryption = True
MQTT_User = 'iottalk'
MQTT_PW = 'iottalk2023'

device_model = 'linebot007'
IDF_list = ['linebot_json_i']
ODF_list = ['linebot_json_o']
device_id = '123456789' #if None, device_id = MAC address
device_name = 'web_skes'
exec_interval = 5  # IDF/ODF interval

import requests, json, time
import config
from model.test_model import model_test_single
last_crying_time = 0

def on_register(r):
    print('Server: {}\nDevice name: {}\nRegister successfully.'.format(r['server'], r['d_name']))

def linebot_json_i():
    global last_crying_time
    response = model_test_single("./model/audio/baby-crying-04.wav", "./model/densenet.pth")
    if response[0][0]>response[0][1]:
        response = 0
    else:
        response = 1
    print("response: ", response)

    if response: # baby is crying
        model_predict_time = time.time()
        print(f'duration = {model_predict_time-last_crying_time}')
        
        if (model_predict_time-last_crying_time)<20:
            return None
        
        last_crying_time = model_predict_time
        selected_music = "babyshark.mp3" # select music name from 's3'
        return {"baby_id": random.choice(["A007", "A008", "A009", "A010", "A101"]), "selected_music": selected_music}
    else:
        return None 

def linebot_json_o(data:list):
    # print("data: ", data) # [{"baby_id": "A007", "selected_music": selected_music}]
    
    if data==None:
        return 0

    selected_music = data[0]["selected_music"]
    
    print("select music: ", selected_music)  # need to get music
    return data

