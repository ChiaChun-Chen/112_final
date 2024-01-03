# from flask import Flask, render_template, request

# app = Flask(__name__, static_folder='static')

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload():
#     audio_file = request.files['audio']

#     return '音檔已接收'

# if __name__ == '__main__':
#     app.run(debug=True)

#-------------------------------------------------
from flask import Flask, render_template, request, jsonify , url_for
import random

from DAI import main as DAI_main
import threading
from model.test_model import model_test_single

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    print('url: ', url_for('static', filename='music/babyshark.mp3'))
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    audio_file = request.form
    print(f'audio url = {audio_file}')
    response = model_test_single(audio_file, "./model/densenet.pth")
    if response[0][0]>response[0][1]:
        response = 0
    else:
        response = 1
    print(f"upload model response = {response}")
    return jsonify({'message': 'Audio file received and processed'})

@app.route('/play_music', methods=['POST'])
def play_music():
    music_dir = 'static/music'
    selected_music = request.json['music_name']
    music_url = f'{music_dir}/{selected_music}'
    return jsonify({'message': music_url})

@app.route('/get_baby_state', methods=['GET']) # fake api for testing idf
def get_baby_state():
    return {'state': random.choice([True, False])}

@app.route('/get_baby_id', methods=['GET'])
def get_baby_id():
    return {"id": random.choice(["A007", "A008", "A009", "A010", "A101"])}

if __name__ == '__main__':
    t = threading.Thread(target=DAI_main)
    t.daemon = True
    t.start()

    app.run(debug=True, port=8089, host="0.0.0.0")



