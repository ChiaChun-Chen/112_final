// let mediaRecorder;
// let audioChunks = [];
// let recordInterval;

// document.getElementById('startButton').addEventListener('click', () => {
//     document.getElementById('startButton').classList.add('btn-pressed');
//     document.getElementById('stopButton').disabled = false;
//     navigator.mediaDevices.getUserMedia({ audio: true })
//         .then(stream => {
//             mediaRecorder = new MediaRecorder(stream);
//             mediaRecorder.addEventListener('dataavailable', event => {
//                 audioChunks.push(event.data);
//             });

//             mediaRecorder.addEventListener('stop', () => {
//                 const audioBlob = new Blob(audioChunks);
//                 sendAudioToServer(audioBlob);
//                 audioChunks = [];
//             });

//             startRecording();
//         });
// });

// document.getElementById('stopButton').addEventListener('click', () => {
//     document.getElementById('startButton').classList.remove('btn-pressed');
//     document.getElementById('stopButton').disabled = true;
//     stopRecordingProcess();
// });

// function startRecording() {
//     audioChunks = [];
//     mediaRecorder.start();
//     
//     setTimeout(() => {
//         if (mediaRecorder.state === 'recording') {
//             mediaRecorder.stop();
//         }
//     }, 7000); // 錄音7s

//     
//     recordInterval = setInterval(() => {
//         if (mediaRecorder.state !== 'recording') {
//             audioChunks = [];
//             mediaRecorder.start();
//             setTimeout(() => {
//                 if (mediaRecorder.state === 'recording') {
//                     mediaRecorder.stop();
//                 }
//             }, 7000); // 錄音7秒
//         }
//     }, 20000); // 每20秒執行一次
// }

// function stopRecordingProcess() {
//     clearInterval(recordInterval);
//     if (mediaRecorder.state === 'recording') {
//         mediaRecorder.stop();
//     }
// }

// function sendAudioToServer(audioBlob) {
//     const formData = new FormData();
//     formData.append('audio', audioBlob);

//     fetch('/upload', {
//         method: 'POST',
//         body: formData
//     }).then(response => {

//         return response.text();
//     }).then(text => {
//         console.log(text);

//     }).catch(error => {
//         console.error(error);
//     });
// }

//-----------------------------

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
                const audioBlob = new Blob(audioChunks, {type: "audio/wav"});
                const audio = new Audio();
                const audioURL = window.URL.createObjectURL(audioBlob);
                console.log("audio url: ", audioURL);
                audio.src = audioURL;
                // saveRecording(audioURL);
                playMusic(audioURL);

                // var reader = new FileReader();
                // babyvoice = reader.readAsBinaryString(audioBlob);
                // console.log("babyvoice = ", babyvoice);

                sendAudioURLToServer(audioURL);
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
    clearInterval(recordInterval);
    if (mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
    }
}

function sendAudioToServer(audioBlob) {
    const formData = new FormData();
    formData.append('audio', audioBlob);
    const audioFile = formData.get('audio');
    console.log('file_context: ',audioFile);
    

    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(response => {

        return response.text();
    }).then(text => {
        console.log(text);

    }).catch(error => {
        console.error(error);
    });
}

function sendAudioURLToServer(audioURL) {
    const formData = new FormData();
    formData.append('audioURL', audioURL);
    const audioFile = formData.get('audioURL');
    console.log('file_context: ',audioFile);
    

    fetch('/upload', {
        method: 'POST',
        body: formData
    }).then(response => {

        return response.text();
    }).then(text => {
        console.log(text);

    }).catch(error => {
        console.error(error);
    });
}

function playMusic(musicUrl) {
    const musicPlayer = document.getElementById('babyMusicPlayer');
    const musicSrc = document.getElementById('musicSrc');
    musicSrc.src = musicUrl;
    musicPlayer.load();
    musicPlayer.play();
    musicPlayer.hidden = false;  
}

var saveRecording = function(url){
    var a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display:none";
    a.href = url;
    a.download = url+'.wav';
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
};