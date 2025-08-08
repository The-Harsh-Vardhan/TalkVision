#!/usr/bin/env python3
"""
Simple Python script to test TalkVision API with audio files
"""

import requests
import json
import os

def test_audio_transcription(audio_file_path):
    """Test transcription with a real audio file"""
    
    # API endpoint
    url = "https://the-harsh-vardhan-talkvision.hf.space/transcribe/"
    
    # Check if file exists
    if not os.path.exists(audio_file_path):
        print(f"❌ Audio file not found: {audio_file_path}")
        return False
    
    print(f"🎵 Testing with audio file: {audio_file_path}")
    print(f"📁 File size: {os.path.getsize(audio_file_path)} bytes")
    
    try:
        # Open and send the audio file
        with open(audio_file_path, 'rb') as audio_file:
            files = {
                'file': (os.path.basename(audio_file_path), audio_file, 'audio/wav')
            }
            
            print("📤 Sending POST request...")
            response = requests.post(url, files=files, timeout=60)
            
            print(f"📊 Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ SUCCESS!")
                print("📝 Transcription Result:")
                print(json.dumps(result, indent=2))
                return True
            else:
                print("❌ FAILED!")
                print(f"Error: {response.text}")
                return False
                
    except requests.exceptions.Timeout:
        print("❌ Request timed out (>60 seconds)")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def test_multiple_files(audio_files):
    """Test multiple audio files"""
    print("🧪 Testing Multiple Audio Files")
    print("=" * 40)
    
    results = []
    for audio_file in audio_files:
        print(f"\n🎧 Testing: {audio_file}")
        print("-" * 30)
        success = test_audio_transcription(audio_file)
        results.append((audio_file, success))
        print()
    
    # Summary
    print("📊 SUMMARY:")
    print("-" * 20)
    for file_path, success in results:
        status = "✅" if success else "❌"
        filename = os.path.basename(file_path)
        print(f"{status} {filename}")

def create_sample_audio_request():
    """Show how to create audio programmatically and test"""
    import numpy as np
    import wave
    import tempfile
    
    print("🎵 Creating sample audio for testing...")
    
    # Create temporary WAV file
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    temp_file.close()
    
    try:
        # Generate a simple sine wave (440 Hz A note)
        duration = 3  # seconds
        sample_rate = 16000
        frequency = 440
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_data = np.sin(2 * np.pi * frequency * t)
        audio_data = (audio_data * 32767).astype(np.int16)
        
        # Write to WAV file
        with wave.open(temp_file.name, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes per sample
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        print(f"✅ Created test audio: {temp_file.name}")
        
        # Test it
        success = test_audio_transcription(temp_file.name)
        
        # Note about sine wave
        if not success:
            print("\n💡 Note: Pure sine waves may not transcribe well.")
            print("   Try with actual speech audio for better results.")
    
    finally:
        # Clean up
        try:
            os.unlink(temp_file.name)
        except:
            pass

def main():
    print("🦻 TalkVision API Audio Testing")
    print("=" * 35)
    
    # Test options
    print("\nChoose testing method:")
    print("1. Test with your own audio file")
    print("2. Test with generated sine wave")
    print("3. Test multiple files")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        # Test with user's audio file
        audio_path = input("\n📁 Enter path to your audio file: ").strip()
        if audio_path:
            test_audio_transcription(audio_path)
        else:
            print("❌ No file path provided")
    
    elif choice == "2":
        # Test with generated audio
        create_sample_audio_request()
    
    elif choice == "3":
        # Test multiple files
        print("\n📁 Enter audio file paths (one per line, empty line to finish):")
        files = []
        while True:
            path = input("File path: ").strip()
            if not path:
                break
            files.append(path)
        
        if files:
            test_multiple_files(files)
        else:
            print("❌ No files provided")
    
    else:
        print("❌ Invalid choice")
    
    print("\n🌐 Alternative Testing Methods:")
    print("1. Use the web interface: https://the-harsh-vardhan-talkvision.hf.space/docs")
    print("2. Use Postman or similar API testing tools")
    print("3. Use the cURL commands from curl_examples.txt")

if __name__ == "__main__":
    main()
