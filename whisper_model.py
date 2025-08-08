# whisper_model.py
import whisper
import os
from typing import Dict, Optional

# Get model type from environment variable, default to "base"
MODEL_TYPE = os.getenv("WHISPER_MODEL", "base")
DEVICE = os.getenv("WHISPER_DEVICE", "cpu")

# Load the model globally so it stays in memory
try:
    model = whisper.load_model(MODEL_TYPE, device=DEVICE)
    print(f"✅ Whisper model '{MODEL_TYPE}' loaded successfully on {DEVICE}")
except Exception as e:
    print(f"❌ Error loading Whisper model: {e}")
    # Fallback to tiny model if the specified model fails
    model = whisper.load_model("tiny", device="cpu")
    print("🔄 Fallback: Loaded 'tiny' model on CPU")

def transcribe_audio(file_path: str, language: Optional[str] = None) -> Dict:
    """
    Transcribe the given audio file and return the result as a dictionary.
    
    Args:
        file_path (str): Path to the audio file
        language (str, optional): Language code (e.g., 'en', 'es', 'fr')
                                If None, auto-detect language
    
    Returns:
        dict: Transcription result with text, segments, and language info
        
    Raises:
        Exception: If transcription fails
    """
    try:
        # Transcribe with or without language specification
        if language:
            result = model.transcribe(file_path, language=language)
        else:
            # Auto-detect language if ENABLE_LANGUAGE_DETECTION is true
            enable_detection = os.getenv("ENABLE_LANGUAGE_DETECTION", "true").lower() == "true"
            if enable_detection:
                result = model.transcribe(file_path)
            else:
                result = model.transcribe(file_path, language="en")
        
        return {
            "text": result["text"].strip(),
            "segments": result.get("segments", []),
            "language": result.get("language", "unknown"),
            "confidence": _calculate_confidence(result.get("segments", []))
        }
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")

def _calculate_confidence(segments: list) -> float:
    """Calculate average confidence score from segments."""
    if not segments:
        return 0.0
    
    confidences = []
    for segment in segments:
        if "avg_logprob" in segment:
            # Convert log probability to confidence (rough approximation)
            confidence = max(0, min(1, (segment["avg_logprob"] + 1)))
            confidences.append(confidence)
    
    return sum(confidences) / len(confidences) if confidences else 0.0

def get_model_info() -> Dict:
    """Get information about the current model."""
    return {
        "model_type": MODEL_TYPE,
        "device": DEVICE,
        "is_multilingual": hasattr(model, 'is_multilingual') and model.is_multilingual
    }