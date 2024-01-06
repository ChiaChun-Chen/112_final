from flask import Flask, render_template, request, jsonify , url_for
import random

from DAI import main as DAI_main
import threading
from model.test_model import main as model_main
import io
import soundfile
import glob

app = Flask(__name__, static_folder='static')
music_to_play = ""
record_status = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/change_record_status', methods=['POST'])
def change_record_status():
    # Since the true/false in javascript is different from True/False in python,
    # so we cannot simply use boolean
    global record_status
    status = request.form.get('record_status')
    print(f'status = {status}')
    if status == "true":
        record_status = True
    else:
        record_status = False
    print(f'record status = {record_status}')
    return {"record status": record_status}

@app.route('/get_record_status', methods=['GET'])
def get_record_status():
    return {"record_status": record_status}

@app.route('/upload', methods=['POST'])
def upload():
    # save wav file into the device
    audio_file = request.files['audio']
    filename = "myRecorder.wav"
    filepath = f"./model/audio/{filename}"
    audio_file.save(filepath)

    # choose music to play randomly
    global music_to_play
    music_list = glob.glob("./static/music/*.mp3")
    music_to_play = random.choice(music_list)

    return jsonify({'message': 'Audio file received and processed', 'music_path': music_to_play})

@app.route('/get_music', methods=['GET'])
def get_music():
    return {"selected_music": music_to_play}

@app.route('/predict_recorder', methods=['GET'])
def predict_recorder():
    # get the record from device with the static file name "myRecorder.wav"
    response = model_main("./model/audio/myRecorder.wav")
    if response[0][0]>response[0][1]:
        response = 0
    else:
        response = 1
    return {"predict_response": response}

@app.route('/play_music', methods=['POST'])
def play_music():
    music_dir = 'static/music'
    selected_music = request.json['music_name']
    music_url = f'{music_dir}/{selected_music}'
    return jsonify({'message': music_url})

if __name__ == '__main__':
    t = threading.Thread(target=DAI_main)
    t.daemon = True
    t.start()

    app.run(debug=True, port=8089, host="127.0.0.1")



