# Hugging Face Spaces Deployment Guide

## Step-by-Step Instructions

### 1. Choose Docker SDK

- Go to [Hugging Face Spaces](https://huggingface.co/spaces)
- Click "Create new Space"
- **Space SDK**: Select **Docker** ⭐
- Space name: `talkvision` (or your preferred name)
- License: MIT
- Make it public

### 2. Upload Files

Upload these files to your Hugging Face Space:

**Required Files:**

- `Dockerfile` ✅
- `app.py` ✅
- `whisper_model.py` ✅
- `utils.py` ✅
- `requirements.txt` ✅
- `README_HF.md` → Rename to `README.md` in the Space

**Optional Files:**

- `test_api.py` (for testing)
- `.env.example` (for reference)

### 3. Configuration

The Space will automatically:

- Build the Docker image
- Install dependencies
- Start the FastAPI server on port 7860
- Load the Whisper model

### 4. Access Your API

Once deployed, your API will be available at:

- **Base URL**: `https://your-username-talkvision.hf.space`
- **Health Check**: `GET /`
- **Transcribe**: `POST /transcribe/`
- **API Docs**: `/docs`

### 5. Test Your Deployment

```bash
# Test health endpoint
curl https://your-username-talkvision.hf.space/

# Test transcription (replace with your Space URL)
curl -X POST "https://your-username-talkvision.hf.space/transcribe/" \
     -F "file=@sample_audio.wav"
```

## Expected Response Format

```json
{
  "transcript": "Your transcribed text here",
  "language": "en",
  "confidence": 0.85,
  "processing_info": {
    "file_name": "sample_audio.wav",
    "file_size": 156234,
    "model_used": "base"
  }
}
```

## Environment Variables (Optional)

You can set these in the Space settings:

- `WHISPER_MODEL`: "tiny", "base", "small" (default: "base")
- `MAX_FILE_SIZE`: Maximum upload size in bytes
- `WHISPER_DEVICE`: "cpu" or "cuda"

## Supported Audio Formats

- WAV
- MP3
- M4A
- FLAC
- OGG

## Performance Notes

- **First request**: May take longer (model loading)
- **Subsequent requests**: Much faster
- **File size limit**: 25MB
- **Processing time**: 2-10 seconds depending on audio length

## Troubleshooting

### Build Fails

- Check `Dockerfile` syntax
- Ensure all files are uploaded
- Check `requirements.txt` format

### Runtime Errors

- Check logs in Space interface
- Verify audio file format
- Test with smaller files first

### Slow Performance

- Use "tiny" model for faster inference
- Reduce audio file size
- Consider shorter audio clips (3-5 seconds)

## Integration Examples

### JavaScript/Web

```javascript
const formData = new FormData();
formData.append("file", audioFile);

fetch("https://your-username-talkvision.hf.space/transcribe/", {
  method: "POST",
  body: formData,
})
  .then((response) => response.json())
  .then((data) => console.log(data.transcript));
```

### Python

```python
import requests

with open('audio.wav', 'rb') as f:
    response = requests.post(
        'https://your-username-talkvision.hf.space/transcribe/',
        files={'file': f}
    )

print(response.json()['transcript'])
```

### ESP32 (Arduino)

```cpp
HTTPClient http;
http.begin("https://your-username-talkvision.hf.space/transcribe/");
http.addHeader("Content-Type", "multipart/form-data");

// Add your audio data
int responseCode = http.POST(audioData);
String response = http.getString();
```

## Next Steps

1. Deploy to Hugging Face Spaces
2. Test with sample audio files
3. Integrate with your ESP32 device
4. Monitor usage and performance
5. Consider upgrading to larger models if needed
