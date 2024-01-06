let mediaRecorder;
let audioChunks = [];
let recordInterval;

document.getElementById('startButton').addEventListener('click', () => {
    document.getElementById('startButton').classList.add('btn-pressed');
    document.getElementById('stopButton').disabled = false;
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.addEventListener('dataavailable', event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener('stop', () => {
                console.log(mediaRecorder.state);
                console.log("recorder stopped");

                // save recorder into blob object with type of wav audio
                const audioBlob = new Blob(audioChunks, {type: "audio/wav"});
                sendAudioToServer(audioBlob);
                audioChunks = [];
            });

            startRecording();
        });
});

document.getElementById('stopButton').addEventListener('click', () => {
    document.getElementById('startButton').classList.remove('btn-pressed');
    document.getElementById('stopButton').disabled = true;
    stopRecordingProcess();
});

function startRecording() {
    audioChunks = [];
    mediaRecorder.start();
    console.log(mediaRecorder.state);
    console.log("recorder started");
    sendRecordStatusToServer("true");

    setTimeout(() => {
        if (mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
        }
    }, 7000); // 錄音7s


    recordInterval = setInterval(() => {
        if (mediaRecorder.state !== 'recording') {
            audioChunks = [];
            mediaRecorder.start();
            console.log(mediaRecorder.state);
            console.log("recorder started");
            setTimeout(() => {
                if (mediaRecorder.state === 'recording') {
                    mediaRecorder.stop();
                }
            }, 7000); // 錄音7秒
        }
    }, 30000); // 每30秒執行一次
}

function stopRecordingProcess() {
    sendRecordStatusToServer("false");
    clearInterval(recordInterval);
    if (mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
    }
}

function sendRecordStatusToServer(status){
    const formData = new FormData();
    formData.append('record_status', status);
    console.log('record status: ', status);

    fetch('/change_record_status', {
        method: 'POST',
        body: formData
    }).then(response => {
        console.log(response)
    })
}

function sendAudioToServer(audioBlob) {
    const formData = new FormData();
    formData.append('audio', audioBlob);
    const audioFile = formData.get('audio');
    console.log('file_context: ',audioFile);
    var music_path = ""
    

    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(response => {
        return response.text();
    }).then(text => {

        // parse the response to get music path to play
        var response = JSON.parse(text);
        console.log("response: ", response['music_path']);
        music_path = response['music_path']
    }).catch(error => {
        console.error(error);
    });

    fetch('/predict_recorder', {
        method: 'GET'
    }).then(response => {
        return response.text();
    }).then(text => {

        // parse the response
        var response = JSON.parse(text);

        // play the music
        if(response['predict_response'] == 1){
            playMusic(music_path);
        }
    }).catch(error => {
        console.error(error);
    });
}

function playMusic(musicPath) {
    const musicPlayer = document.getElementById('babyMusicPlayer');
    const musicSrc = document.getElementById('musicSrc');
    musicSrc.src = musicPath;
    musicPlayer.load();
    musicPlayer.play();
    musicPlayer.hidden = false;  
}