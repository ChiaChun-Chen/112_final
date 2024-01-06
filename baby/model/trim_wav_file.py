import librosa
import soundfile as sf #負責寫音檔

def trim_audio(input_file, output_file, time=5):
    # 讀音檔
    audio, _ = librosa.load(input_file)
    sr = 22050
    audio, _ = librosa.effects.trim(audio,top_db=60) 
    new_audio = sr * time
    # 擷取5秒
    trimmed_audio = audio[:new_audio]

    # 存檔
    sf.write(output_file, trimmed_audio, sr)
    