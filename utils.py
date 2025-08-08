import whisper
import soundfile as sf
import io

# Load model globally to avoid reloading each request
model = whisper.load_model("base")

def save_temp_audio(audio_bytes, filename="temp.wav"):
    with open(filename, "wb") as f:
        f.write(audio_bytes)
    return filename

def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]

def audio_bytes_to_wav(audio_bytes, output_path="temp.wav"):
    data, samplerate = sf.read(io.BytesIO(audio_bytes))
    sf.write(output_path, data, samplerate)
    return output_path