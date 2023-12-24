import random 
from LineBot_basic import read_message, send_mesage, main

ServerURL = 'https://class.iottalk.tw' #For example: 'https://iottalk.tw'
MQTT_broker = 'class.iottalk.tw' # MQTT Broker address, for example:  'iottalk.tw' or None = no MQTT support
MQTT_port = 5566
MQTT_encryption = True
MQTT_User = 'iottalk'
MQTT_PW = 'iottalk2023'

device_model = 'linebot007'
IDF_list = ['linebot_json_i']
ODF_list = ['linebot_json_o']
device_id = '12345678910' #if None, device_id = MAC address
device_name = 'linebot_skes'
exec_interval = 1  # IDF/ODF interval

import requests, json
import config
web_line_dict = {"A007": config.A007_LINEID, 
                 "A010": config.A010_LINEID,
                 "A101": config.A101_LINEID}

def on_register(r):
    print('Server: {}\nDevice name: {}\nRegister successfully.'.format(r['server'], r['d_name']))

def linebot_json_i():
    response = requests.get(f'{config.APP_URL}/get_baby_state')
    response = response.json()["state"]

    baby_id = requests.get(f'{config.APP_URL}/get_baby_id').json()["id"]
    if baby_id in web_line_dict.keys():
        user_id = web_line_dict[baby_id]
    else:
        return None # End

    if response: # baby is crying
        selected_music = "babyshark.mp3" # select music name from 's3'
        return {"user_id": user_id, "selected_music": selected_music}
    else:
        return None 

def linebot_json_o(data:list):
    print("data: ", data) # [[{'user_id': 'id', 'selected_music': 'babyshark.mp3'}, {'need_to_change_music': False}]]
    need_to_change_music = data[0][1]["need_to_change_music"]
    if need_to_change_music:
        selected_music = data[0][0]["selected_music"]
        try:
            response = requests.post(f'{config.APP_URL}/play_music', json={'music_name': selected_music})
            if response.status_code == 200:
                print(f'Music {selected_music} play request sent successfully.')
            else:
                print('Failed to send music play request.')
        except Exception as e:
            print(f'Error: {e}')

        send_mesage(data[0][0]["user_id"], f"您的寶寶在哭泣! 正在為您撥放音樂: {selected_music}") # send notify to parent's line through linebot
