from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from whisper_model import transcribe_audio, get_model_info
import os
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="TalkVision API", 
    description="Real-time speech-to-text for hearing-impaired using Whisper ASR",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for web frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "TalkVision API is running",
        "status": "healthy",
        "model_info": get_model_info()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        model_info = get_model_info()
        return {
            "status": "healthy",
            "api_version": "1.0.0",
            "whisper_model": model_info["model_type"],
            "device": model_info["device"]
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    """Transcribe audio file to text"""
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file size (25MB limit)
    max_size = int(os.getenv("MAX_FILE_SIZE", 26214400))  # 25MB default
    if file.size and file.size > max_size:
        raise HTTPException(status_code=413, detail=f"File too large. Maximum size: {max_size} bytes")
    
    # Validate file type
    allowed_types = ["audio/wav", "audio/mpeg", "audio/mp3", "audio/m4a", "audio/flac", "audio/ogg"]
    if file.content_type and file.content_type not in allowed_types:
        logger.warning(f"Received file with content type: {file.content_type}")
        # Don't reject - some valid audio files might have incorrect content types
    
    temp_file_path = None
    try:
        logger.info(f"Processing audio file: {file.filename}")
        
        # Read audio data
        audio_data = await file.read()
        logger.info(f"File size: {len(audio_data)} bytes")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
        
        logger.info(f"Created temporary file: {temp_file_path}")
        
        # Transcribe audio
        result = transcribe_audio(temp_file_path)
        
        logger.info(f"Transcription completed. Text length: {len(result['text'])}")
        
        # Return enhanced response
        return {
            "transcript": result["text"],
            "language": result.get("language", "unknown"),
            "confidence": result.get("confidence", 0.0),
            "processing_info": {
                "file_name": file.filename,
                "file_size": len(audio_data),
                "model_used": get_model_info()["model_type"]
            }
        }
    
    except Exception as e:
        logger.error(f"Transcription failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
    
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                logger.info(f"Cleaned up temporary file: {temp_file_path}")
            except Exception as cleanup_error:
                logger.warning(f"Failed to cleanup temp file: {cleanup_error}")

@app.get("/info")
async def model_info():
    """Get model information"""
    return get_model_info()

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)