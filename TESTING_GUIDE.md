# 🧪 TalkVision API Testing Guide

## ✅ Basic API Testing (Already Confirmed Working)

Your TalkVision API is successfully deployed and the basic endpoints are working:

### 1. Health Check ✅

- **URL**: https://the-harsh-vardhan-talkvision.hf.space/
- **Expected Response**:

```json
{
  "message": "TalkVision API is running",
  "status": "healthy",
  "model_info": {
    "model_type": "base",
    "device": "cpu",
    "is_multilingual": true
  }
}
```

### 2. Model Information ✅

- **URL**: https://the-harsh-vardhan-talkvision.hf.space/info
- **Expected Response**:

```json
{
  "model_type": "base",
  "device": "cpu",
  "is_multilingual": true
}
```

### 3. Detailed Health ✅

- **URL**: https://the-harsh-vardhan-talkvision.hf.space/health
- **Expected Response**:

```json
{
  "status": "healthy",
  "api_version": "1.0.0",
  "whisper_model": "base",
  "device": "cpu"
}
```

## 🎙️ Audio Transcription Testing

### Interactive Testing (Recommended)

1. **Open API Documentation**: https://the-harsh-vardhan-talkvision.hf.space/docs
2. **Find the `/transcribe/` endpoint**
3. **Click "Try it out"**
4. **Upload an audio file** (WAV, MP3, M4A, FLAC supported)
5. **Click "Execute"**

### Manual cURL Testing

```bash
# Test with your own audio file
curl -X POST "https://the-harsh-vardhan-talkvision.hf.space/transcribe/" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_audio_file.wav"
```

### Expected Transcription Response

```json
{
  "transcript": "Your transcribed text will appear here",
  "language": "en",
  "confidence": 0.85,
  "processing_info": {
    "file_name": "your_audio_file.wav",
    "file_size": 156234,
    "model_used": "base"
  }
}
```

## 🔧 Testing Different Scenarios

### 1. Test Valid Audio Files

- ✅ WAV files (recommended)
- ✅ MP3 files
- ✅ M4A files
- ✅ FLAC files
- ✅ OGG files

### 2. Test File Size Limits

- ✅ Small files (< 1MB) - Should work fast
- ✅ Medium files (1-10MB) - Should work normally
- ⚠️ Large files (10-25MB) - Should work but slower
- ❌ Very large files (>25MB) - Should be rejected

### 3. Test Error Handling

- ❌ No file uploaded - Should return 400 error
- ❌ Invalid file format - Should return 400/415 error
- ❌ Corrupted audio - Should return 500 error

### 4. Test Audio Quality

- ✅ Clear speech - High accuracy expected
- ⚠️ Noisy audio - Lower accuracy expected
- ⚠️ Multiple speakers - May have challenges
- ⚠️ Background music - May affect accuracy

## 📱 ESP32 Integration Testing

### Test URL for ESP32

```cpp
// Use this URL in your ESP32 code
const char* serverURL = "https://the-harsh-vardhan-talkvision.hf.space/transcribe/";
```

### ESP32 Test Code Example

```cpp
#include <HTTPClient.h>
#include <WiFi.h>

void testTalkVisionAPI() {
    HTTPClient http;
    http.begin("https://the-harsh-vardhan-talkvision.hf.space/transcribe/");
    http.addHeader("Content-Type", "multipart/form-data");

    // Add your audio data here
    // int httpResponseCode = http.POST(audioData);

    // For now, test health endpoint
    http.begin("https://the-harsh-vardhan-talkvision.hf.space/");
    int httpResponseCode = http.GET();

    if (httpResponseCode > 0) {
        String response = http.getString();
        Serial.println("API Response: " + response);
    }

    http.end();
}
```

## 🚀 Performance Testing

### Response Time Benchmarks

- **Health endpoints**: < 1 second
- **Audio transcription**: 2-10 seconds (depends on audio length)
- **First request**: May take longer (model initialization)

### Concurrent Testing

- Test multiple requests simultaneously
- Check if the API handles load properly
- Monitor response times under load

## 🐛 Common Issues & Solutions

### 1. Timeout Errors

- **Cause**: Large audio files or slow network
- **Solution**: Use smaller audio chunks (3-5 seconds)

### 2. Format Errors

- **Cause**: Unsupported audio format
- **Solution**: Convert to WAV or MP3

### 3. Size Errors

- **Cause**: File too large (>25MB)
- **Solution**: Compress audio or split into chunks

### 4. Quality Issues

- **Cause**: Poor audio quality
- **Solution**: Improve microphone setup, reduce noise

## ✅ Testing Checklist

- [ ] Health endpoint responds correctly
- [ ] Model info endpoint works
- [ ] API documentation is accessible
- [ ] Can upload and transcribe a WAV file
- [ ] Can upload and transcribe an MP3 file
- [ ] Error handling works for invalid files
- [ ] Response includes all expected fields
- [ ] Transcription accuracy is acceptable
- [ ] Response time is reasonable
- [ ] CORS headers allow web requests

## 🎯 Next Steps for Production

1. **Test with real ESP32 device**
2. **Test with various audio qualities**
3. **Monitor API usage and performance**
4. **Set up monitoring/alerts**
5. **Consider rate limiting for production use**

## 📞 Support

If you encounter issues:

1. Check the logs in Hugging Face Spaces
2. Test with different audio files
3. Verify file formats and sizes
4. Check network connectivity

Your TalkVision API is ready for real-world testing! 🎉
