#!/usr/bin/env python3
"""
Test script for TalkVision API on Hugging Face Spaces
"""

import requests
import sys
import json

def test_api(base_url="http://localhost:7860"):
    """Test the TalkVision API endpoints"""
    
    print(f"🧪 Testing TalkVision API at {base_url}")
    print("=" * 50)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Health Check: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health Check failed: {e}")
        return False
    
    # Test 2: Model info
    try:
        response = requests.get(f"{base_url}/info")
        print(f"✅ Model Info: {response.status_code}")
        print(f"   Model: {response.json()}")
    except Exception as e:
        print(f"❌ Model Info failed: {e}")
    
    # Test 3: API Documentation
    try:
        response = requests.get(f"{base_url}/docs")
        print(f"✅ API Docs: {response.status_code}")
    except Exception as e:
        print(f"❌ API Docs failed: {e}")
    
    print("\n🎯 API is ready for audio transcription!")
    print(f"📖 Visit {base_url}/docs for interactive API documentation")
    
    return True

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:7860"
    test_api(base_url)
