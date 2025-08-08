#!/usr/bin/env python3
"""
Comprehensive test script for TalkVision API
Tests both local and deployed versions
"""

import requests
import json
import time
import sys
import os
from pathlib import Path

# Test configurations
LOCAL_URL = "http://127.0.0.1:8000"
DEPLOYED_URL = "https://the-harsh-vardhan-talkvision.hf.space"

class TalkVisionTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
    
    def log_test(self, test_name, success, details=""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   {details}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details
        })
    
    def test_health_endpoint(self):
        """Test the root health endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                expected_keys = ["message", "status", "model_info"]
                if all(key in data for key in expected_keys):
                    self.log_test("Health Endpoint", True, f"Status: {data['status']}, Model: {data['model_info']['model_type']}")
                else:
                    self.log_test("Health Endpoint", False, f"Missing keys in response: {data}")
            else:
                self.log_test("Health Endpoint", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Health Endpoint", False, f"Exception: {str(e)}")
    
    def test_detailed_health(self):
        """Test the detailed health endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                expected_keys = ["status", "api_version", "whisper_model", "device"]
                if all(key in data for key in expected_keys):
                    self.log_test("Detailed Health", True, f"API v{data['api_version']}, Model: {data['whisper_model']}")
                else:
                    self.log_test("Detailed Health", False, f"Missing keys: {data}")
            else:
                self.log_test("Detailed Health", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Detailed Health", False, f"Exception: {str(e)}")
    
    def test_model_info(self):
        """Test the model info endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/info")
            if response.status_code == 200:
                data = response.json()
                expected_keys = ["model_type", "device", "is_multilingual"]
                if all(key in data for key in expected_keys):
                    self.log_test("Model Info", True, f"Model: {data['model_type']}, Multilingual: {data['is_multilingual']}")
                else:
                    self.log_test("Model Info", False, f"Missing keys: {data}")
            else:
                self.log_test("Model Info", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Model Info", False, f"Exception: {str(e)}")
    
    def test_api_docs(self):
        """Test API documentation availability"""
        try:
            response = self.session.get(f"{self.base_url}/docs")
            if response.status_code == 200:
                self.log_test("API Documentation", True, "Swagger UI accessible")
            else:
                self.log_test("API Documentation", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("API Documentation", False, f"Exception: {str(e)}")
    
    def test_transcribe_invalid_file(self):
        """Test transcribe endpoint with invalid file"""
        try:
            # Test with no file
            response = self.session.post(f"{self.base_url}/transcribe/")
            if response.status_code == 422:  # Validation error expected
                self.log_test("Invalid File Handling", True, "Correctly rejected empty request")
            else:
                self.log_test("Invalid File Handling", False, f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_test("Invalid File Handling", False, f"Exception: {str(e)}")
    
    def test_transcribe_text_file(self):
        """Test transcribe endpoint with non-audio file"""
        try:
            # Create a dummy text file
            test_content = "This is not an audio file"
            files = {'file': ('test.txt', test_content, 'text/plain')}
            
            response = self.session.post(f"{self.base_url}/transcribe/", files=files)
            # Should either process or reject gracefully
            if response.status_code in [400, 415, 500]:  # Expected error codes
                self.log_test("Non-Audio File Handling", True, f"Correctly handled non-audio file (HTTP {response.status_code})")
            else:
                self.log_test("Non-Audio File Handling", False, f"Unexpected response: {response.status_code}")
        except Exception as e:
            self.log_test("Non-Audio File Handling", False, f"Exception: {str(e)}")
    
    def test_cors_headers(self):
        """Test CORS headers"""
        try:
            response = self.session.options(f"{self.base_url}/")
            cors_headers = ['Access-Control-Allow-Origin', 'Access-Control-Allow-Methods']
            present_headers = [h for h in cors_headers if h in response.headers]
            
            if len(present_headers) > 0:
                self.log_test("CORS Headers", True, f"CORS configured: {present_headers}")
            else:
                self.log_test("CORS Headers", False, "No CORS headers found")
        except Exception as e:
            self.log_test("CORS Headers", False, f"Exception: {str(e)}")
    
    def test_response_time(self):
        """Test API response time"""
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/")
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200:
                if response_time < 5000:  # Less than 5 seconds
                    self.log_test("Response Time", True, f"{response_time:.2f}ms")
                else:
                    self.log_test("Response Time", False, f"Slow response: {response_time:.2f}ms")
            else:
                self.log_test("Response Time", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Response Time", False, f"Exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests"""
        print(f"\n🧪 Testing TalkVision API at: {self.base_url}")
        print("=" * 60)
        
        self.test_health_endpoint()
        self.test_detailed_health()
        self.test_model_info()
        self.test_api_docs()
        self.test_transcribe_invalid_file()
        self.test_transcribe_text_file()
        self.test_cors_headers()
        self.test_response_time()
        
        # Summary
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        print(f"\n📊 Test Summary: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed!")
        else:
            print("⚠️  Some tests failed. Check the details above.")
        
        return passed == total

def main():
    print("🦻 TalkVision API Test Suite")
    print("=" * 40)
    
    # Test deployed version
    print("\n🌐 Testing Deployed API (Hugging Face Spaces)")
    deployed_tester = TalkVisionTester(DEPLOYED_URL)
    deployed_success = deployed_tester.run_all_tests()
    
    # Ask if user wants to test local version
    test_local = input("\n❓ Do you want to test local development server? (y/n): ").lower().strip()
    
    if test_local == 'y':
        print("\n💻 Testing Local API")
        local_tester = TalkVisionTester(LOCAL_URL)
        local_success = local_tester.run_all_tests()
    
    # Final summary
    print("\n" + "=" * 60)
    print("🏁 FINAL RESULTS:")
    print(f"🌐 Deployed API: {'✅ HEALTHY' if deployed_success else '❌ ISSUES FOUND'}")
    
    if test_local == 'y':
        print(f"💻 Local API: {'✅ HEALTHY' if local_success else '❌ ISSUES FOUND'}")
    
    print("\n🔗 Useful Links:")
    print(f"📖 API Docs: {DEPLOYED_URL}/docs")
    print(f"🔍 Health Check: {DEPLOYED_URL}/health")
    print(f"ℹ️  Model Info: {DEPLOYED_URL}/info")

if __name__ == "__main__":
    main()
