#!/usr/bin/env python3
"""
TalkVision Audio Transcription Tester
Tests the main transcription functionality
"""

import requests
import json
import numpy as np
import wave
import tempfile
import os

def create_test_audio(filename, duration=3, sample_rate=16000):
    """Create a simple test audio file (sine wave)"""
    try:
        # Generate a simple sine wave
        t = np.linspace(0, duration, int(sample_rate * duration))
        frequency = 440  # A note
        audio_data = np.sin(2 * np.pi * frequency * t)
        
        # Normalize to 16-bit range
        audio_data = (audio_data * 32767).astype(np.int16)
        
        # Write to WAV file
        with wave.open(filename, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes per sample
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        return True
    except Exception as e:
        print(f"Error creating test audio: {e}")
        return False

def test_transcription_api(audio_file_path):
    """Test the transcription API with an audio file"""
    url = "https://the-harsh-vardhan-talkvision.hf.space/transcribe/"
    
    try:
        with open(audio_file_path, 'rb') as audio_file:
            files = {'file': ('test_audio.wav', audio_file, 'audio/wav')}
            
            print("Sending request to transcription API...")
            response = requests.post(url, files=files, timeout=60)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Transcription successful!")
                print(f"Response: {json.dumps(result, indent=2)}")
                return True
            else:
                print("❌ Transcription failed!")
                print(f"Error: {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_api_endpoints():
    """Test basic API endpoints"""
    base_url = "https://the-harsh-vardhan-talkvision.hf.space"
    
    print("🔍 Testing API Endpoints...")
    print("-" * 30)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ Health endpoint working")
            print(f"   Model: {data.get('model_info', {}).get('model_type', 'unknown')}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    # Test docs endpoint
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print("✅ API documentation accessible")
        else:
            print(f"❌ API docs failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API docs error: {e}")

def main():
    print("🦻 TalkVision Audio Transcription Test")
    print("=" * 45)
    
    # First test basic endpoints
    test_api_endpoints()
    
    print("\n🎵 Testing Audio Transcription...")
    print("-" * 30)
    
    # Create a temporary audio file
    temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    temp_audio.close()
    
    try:
        # Create test audio
        print("Creating test audio file...")
        if create_test_audio(temp_audio.name):
            print(f"✅ Test audio created: {temp_audio.name}")
            
            # Test transcription
            success = test_transcription_api(temp_audio.name)
            
            if success:
                print("\n🎉 Audio transcription test PASSED!")
            else:
                print("\n⚠️  Audio transcription test FAILED!")
        else:
            print("❌ Failed to create test audio")
            
    finally:
        # Clean up
        try:
            os.unlink(temp_audio.name)
        except:
            pass
    
    print("\n📖 Manual Testing:")
    print("1. Visit: https://the-harsh-vardhan-talkvision.hf.space/docs")
    print("2. Try the /transcribe/ endpoint with a real audio file")
    print("3. Check the interactive API documentation")

if __name__ == "__main__":
    main()
