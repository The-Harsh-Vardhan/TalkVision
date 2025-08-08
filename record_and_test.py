#!/usr/bin/env python3
"""
Record audio from microphone and test TalkVision API
"""

import requests
import json
import tempfile
import os

def record_and_test():
    """Record audio from microphone and test the API"""
    try:
        import sounddevice as sd
        import scipy.io.wavfile as wav
        import numpy as np
    except ImportError:
        print("❌ Required packages not installed.")
        print("Install with: pip install sounddevice scipy numpy")
        return False
    
    print("🎤 Recording Audio for TalkVision Test")
    print("=" * 40)
    
    # Recording parameters
    duration = 5  # seconds
    sample_rate = 16000  # Hz
    
    print(f"🔴 Recording for {duration} seconds...")
    print("   Speak clearly into your microphone!")
    
    # Record audio
    audio_data = sd.rec(int(duration * sample_rate), 
                       samplerate=sample_rate, 
                       channels=1, 
                       dtype=np.int16)
    sd.wait()  # Wait until recording is finished
    
    print("✅ Recording completed!")
    
    # Save to temporary file
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    wav.write(temp_file.name, sample_rate, audio_data)
    temp_file.close()
    
    try:
        print(f"💾 Audio saved to: {temp_file.name}")
        print(f"📁 File size: {os.path.getsize(temp_file.name)} bytes")
        
        # Test the API
        print("\n📤 Sending to TalkVision API...")
        success = test_transcription(temp_file.name)
        
        if success:
            print("🎉 Recording and transcription successful!")
        else:
            print("⚠️  Transcription failed. Try speaking more clearly.")
    
    finally:
        # Clean up
        try:
            os.unlink(temp_file.name)
        except:
            pass
    
    return success

def test_transcription(audio_file_path):
    """Test the API with an audio file"""
    url = "https://the-harsh-vardhan-talkvision.hf.space/transcribe/"
    
    try:
        with open(audio_file_path, 'rb') as audio_file:
            files = {'file': ('recorded_audio.wav', audio_file, 'audio/wav')}
            
            response = requests.post(url, files=files, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Transcription Result:")
                print(f"📝 Text: '{result['transcript']}'")
                print(f"🌍 Language: {result.get('language', 'unknown')}")
                print(f"📊 Confidence: {result.get('confidence', 0):.2f}")
                return True
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Details: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    record_and_test()
