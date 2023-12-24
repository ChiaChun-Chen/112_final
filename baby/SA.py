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
exec_interval = 1  # IDF/ODF interval

import requests, json, time
import config
start_crying_time = 0

def on_register(r):
    print('Server: {}\nDevice name: {}\nRegister successfully.'.format(r['server'], r['d_name']))

def linebot_json_i():
    response = requests.get(f'{config.APP_URL}/get_baby_state')
    response = response.json()["state"]

    global start_crying_time
    duration = time.time() - start_crying_time

    if response and (duration>120): # baby is crying and duration time is larger than 2 minutes
        start_crying_time = time.time()
        return {"need_to_change_music": True}

    return {"need_to_change_music": False}

def linebot_json_o(data:list):
    print("data: ", data) # [[{'user_id': 'id', 'selected_music': 'babyshark.mp3'}, {'need_to_change_music': False}]]
    selected_music = data[0][0]["selected_music"]
    need_to_change_music = data[0][1]["need_to_change_music"]
    if need_to_change_music:
        print("select music: ", selected_music)  # need to get music

