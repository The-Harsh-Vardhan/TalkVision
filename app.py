from fastapi import FastAPI, File, UploadFile, HTTPException
from whisper_model import transcribe_audio
import os
import tempfile

app = FastAPI(title="TalkVision API", description="Real-time speech-to-text for hearing-impaired")

@app.get("/")
async def root():
    return {"message": "TalkVision API is running"}

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type or not file.content_type.startswith('audio/'):
        raise HTTPException(status_code=400, detail="File must be an audio file")
    
    try:
        # Read audio data
        audio_data = await file.read()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
        
        # Transcribe audio
        result = transcribe_audio(temp_file_path)
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        return {"transcript": result["text"]}
    
    except Exception as e:
        # Clean up temporary file if it exists
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")