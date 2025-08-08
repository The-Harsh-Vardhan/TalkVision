#!/usr/bin/env python3
"""
Simple TalkVision API Tester
"""

import requests
import json

def test_endpoint(url, name):
    """Test a single endpoint"""
    try:
        print(f"Testing {name}...")
        response = requests.get(url, timeout=10)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"  Response: {json.dumps(data, indent=2)}")
                return True
            except:
                print(f"  Response (text): {response.text[:200]}")
                return True
        else:
            print(f"  Error: {response.text}")
            return False
    except Exception as e:
        print(f"  Failed: {str(e)}")
        return False

def main():
    base_url = "https://the-harsh-vardhan-talkvision.hf.space"
    
    print("🦻 TalkVision API Quick Test")
    print("=" * 40)
    
    # Test endpoints
    endpoints = [
        (f"{base_url}/", "Health Check"),
        (f"{base_url}/health", "Detailed Health"),
        (f"{base_url}/info", "Model Info"),
        (f"{base_url}/docs", "API Documentation")
    ]
    
    results = []
    for url, name in endpoints:
        success = test_endpoint(url, name)
        results.append((name, success))
        print()
    
    # Summary
    print("=" * 40)
    print("SUMMARY:")
    for name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {name}")
    
    passed = sum(1 for _, success in results if success)
    print(f"\nResults: {passed}/{len(results)} endpoints working")

if __name__ == "__main__":
    main()
