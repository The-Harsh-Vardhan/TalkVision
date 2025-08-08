---
title: TalkVision
emoji: 🦻
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# TalkVision: Smart Wearable Subtitles API

Real-time speech-to-text API for hearing-impaired individuals using OpenAI Whisper.

## Usage

### Test the API

- **Health Check**: `GET /`
- **Transcribe Audio**: `POST /transcribe/`
- **API Documentation**: `/docs`

### Example Request

```bash
curl -X POST "https://your-space-name.hf.space/transcribe/" \
     -F "file=@your_audio.wav"
```

### Response

```json
{
  "transcript": "Your transcribed text here"
}
```

This Space runs a FastAPI server that accepts audio files and returns transcribed text using Whisper ASR.
