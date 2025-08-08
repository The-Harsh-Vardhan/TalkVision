from fastapi import FastAPI, File, UploadFile
import whisper

app = FastAPI()
model = whisper.load_model("base")  # you can also try "tiny" for faster inference

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    audio = await file.read()
    with open("temp.wav", "wb") as f:
        f.write(audio)
    result = model.transcribe("temp.wav")
    return {"transcript": result["text"]}