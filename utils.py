import soundfile as sf
import io
import tempfile
import os

def save_temp_audio(audio_bytes, filename="temp.wav"):
    """Save audio bytes to a temporary file."""
    with open(filename, "wb") as f:
        f.write(audio_bytes)
    return filename

def audio_bytes_to_wav(audio_bytes, output_path=None):
    """Convert audio bytes to WAV format."""
    if output_path is None:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        output_path = temp_file.name
        temp_file.close()
    
    try:
        data, samplerate = sf.read(io.BytesIO(audio_bytes))
        sf.write(output_path, data, samplerate)
        return output_path
    except Exception as e:
        if os.path.exists(output_path):
            os.unlink(output_path)
        raise e