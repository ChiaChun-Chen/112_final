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
device_id = 'A007' #if None, device_id = MAC address
device_name = 'web_skes'
exec_interval = 5  # IDF/ODF interval

import requests, json, time
import config
last_crying_time = 0

def on_register(r):
    print('Server: {}\nDevice name: {}\nRegister successfully.'.format(r['server'], r['d_name']))

def linebot_json_i():
    # call api to get the record status
    # if record status is false, then don't do anything
    record_status = requests.get(f'{config.APP_URL}/get_record_status').json()["record_status"]
    if record_status == False:
        print(record_status)
        return None
    print(record_status)
    # need to sleep for 30 seconds if the baby had cried
    global last_crying_time
    model_predict_time = time.time()
    print(f'duration = {model_predict_time-last_crying_time}')
    if (model_predict_time-last_crying_time)<30:
        return None
    
    # call api to get the model predict
    response = requests.get(f'{config.APP_URL}/get_predict_status').json()["predict_status"]

    if response == 1: # baby is crying
        last_crying_time = model_predict_time
        print(requests.get(f'{config.APP_URL}/get_music').json())
        selected_music = requests.get(f'{config.APP_URL}/get_music').json()["selected_music"]
        return {"baby_id": device_id, "selected_music": selected_music}
    else:
        return None 

def linebot_json_o(data:list):
    
    print(data[0])

