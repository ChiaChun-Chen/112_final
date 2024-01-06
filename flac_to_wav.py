from pydub import AudioSegment
import os

def convert_flac_to_wav(input_folder, output_folder):
    for file in os.listdir(input_folder):
        if file.endswith(".3gp"):
            _3gp_path = os.path.join(input_folder, file)
            wav_path = os.path.join(output_folder, os.path.splitext(file)[0] + ".wav")

            audio = AudioSegment.from_file(_3gp_path, format="3gp")
            audio.export(wav_path, format="wav")

if __name__ == "__main__":
    input_folder = "donateacry-android-upload-bucket"
    output_folder = "donateacry-android-upload-bucket_wav"
    convert_flac_to_wav(input_folder, output_folder)