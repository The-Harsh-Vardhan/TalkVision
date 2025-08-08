# 🦻 TalkVision: Smart Wearable Subtitles for the Hearing-Impaired

**TalkVision** is an AI-powered smart wearable designed to empower the hearing-impaired by providing **real-time subtitles** of spoken language through an IoT-enabled device and cloud-based speech-to-text processing. This repository contains the **cloud software backend** built using **FastAPI** and **Whisper ASR**, which processes short audio clips sent from an ESP32-based wearable and returns transcribed subtitles in JSON format.

---

## 📌 Project Features

- 🎙️ Accepts small audio chunks (`.wav`) from an IoT device over HTTP POST
- 🧠 Processes speech using OpenAI’s **Whisper** ASR (Tiny/Base models)
- 🌐 Deployable to **Render**, **Railway**, or any cloud with Python support
- 📤 Returns real-time subtitles in **JSON** for immediate display
- 📱 ESP32-C6 acts as the IoT client, with OLED subtitle rendering
- 📦 Lightweight & Free-tier friendly (edge deployable)

---

## 🚀 How It Works

1. ESP32-C6 captures 3–5 second audio via onboard mic
2. Audio is posted to the cloud API using HTTP
3. Whisper model transcribes the audio to text
4. JSON response with the transcript is sent back
5. ESP32 parses JSON and displays subtitle on OLED in real-time

---

## 🧰 Tech Stack

| Component          | Tech Used               |
| ------------------ | ----------------------- |
| Cloud Framework    | FastAPI (Python)        |
| Speech Recognition | Whisper ASR (Tiny/Base) |
| Deployment         | Render / Railway        |
| IoT Device         | ESP32-C6-DEVKITC-1-N8   |
| Display            | OLED (via Ray Optics)   |
| Format             | JSON                    |

---

## 🛠️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/talkvision-backend.git
cd talkvision-backend
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server locally

```bash
uvicorn app:app --reload
```

### 4. Deploy to Render

Create a new Web Service

Use uvicorn app:app --host 0.0.0.0 --port 10000 as Start Command

Ensure Whisper and Torch are supported (Render supports GPU options)

## 📡 API Endpoint

POST /transcribe/

Field Type Description
file audio/wav Audio chunk uploaded via POST

Response:

json
Copy
Edit
{
"transcript": "This is your subtitle in real-time."
}
