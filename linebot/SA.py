import random, time
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
exec_interval = 5  # IDF/ODF interval

import requests, json
import config
web_line_dict = {"A007": config.A007_LINEID}
                #  "A010": config.A010_LINEID,
                #  "A101": config.A101_LINEID}

def on_register(r):
    print('Server: {}\nDevice name: {}\nRegister successfully.'.format(r['server'], r['d_name']))

def linebot_json_i():
    return None

def linebot_json_o(data:list):
    print("data: ", data) # [{"baby_id": "A007", "selected_music": selected_music}]
    
    if data==None:
        return 0

    baby_id = data[0]["baby_id"]
    if baby_id in web_line_dict.keys():
        user_id = web_line_dict[baby_id]
        selected_music = data[0]["selected_music"]
        try:
            response = requests.post(f'{config.APP_URL}/play_music', json={'music_name': selected_music})
            if response.status_code == 200:
                print(f'Music {selected_music} play request sent successfully.')
            else:
                print('Failed to send music play request.')
        except Exception as e:
            print(f'Error: {e}')

        send_mesage(user_id, f"您的寶寶在哭泣! 正在為您撥放音樂: {selected_music}") # send notify to parent's line through linebot
    return data
