#!/usr/bin/env python3
"""
CareerMatch Backend Test Script
Tests the FastAPI backend with sample quiz data to verify Claude AI integration
"""

import requests
import json
import time
from typing import Dict, Any

# Backend API URL (update this to your deployed URL or localhost)
API_BASE_URL = "https://career-match-0pw6.onrender.com"

def test_backend_health():
    """Test if the backend is running and accessible"""
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"✅ Backend Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend Health Check Failed: {e}")
        return False

def test_career_match(sample_data: Dict[str, Any]) -> bool:
    """Test the career match endpoint with sample quiz data"""
    try:
        print(f"\n🧪 Testing Career Match with sample data...")
        print(f"Sample Data: {json.dumps(sample_data, indent=2)}")
        
        response = requests.post(
            f"{API_BASE_URL}/match",
            headers={"Content-Type": "application/json"},
            json=sample_data,
            timeout=30  # Increased timeout for AI processing
        )
        
        print(f"✅ Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Career Match Result:")
            print(f"   Personality Label: {result.get('personality_label', 'N/A')}")
            print(f"   Job Matches: {result.get('job_matches', [])}")
            print(f"   Strengths: {result.get('strengths', [])}")
            print(f"   Growth Area: {result.get('growth_area', 'N/A')}")
            print(f"   Explanation: {result.get('explanation', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ Error Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Failed: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON Decode Error: {e}")
        return False

def test_multiple_personalities():
    """Test different personality types to verify AI responses"""
    
    test_cases = [
        {
            "name": "Creative Extrovert",
            "data": {
                "personality": "Creative and imaginative",
                "weekend": "Exploring new places and activities",
                "solving": "Intuitive and creative",
                "environment": "Flexible and adaptable",
                "role": "As a leader, taking charge",
                "motivates": "Learning and personal growth"
            }
        },
        {
            "name": "Analytical Introvert",
            "data": {
                "personality": "Reserved and thoughtful",
                "weekend": "Relaxing at home with hobbies",
                "solving": "Analytical and detail-oriented",
                "environment": "Structured and organized",
                "role": "Independently, with minimal interaction",
                "motivates": "Achieving goals and recognition"
            }
        },
        {
            "name": "Practical Team Player",
            "data": {
                "personality": "Practical and organized",
                "weekend": "Spending time with friends and family",
                "solving": "Collaborative and brainstorming-focused",
                "environment": "Collaborative and team-oriented",
                "role": "As a team player, contributing ideas",
                "motivates": "Making a positive impact"
            }
        }
    ]
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*50}")
        print(f"Test Case {i}: {test_case['name']}")
        print(f"{'='*50}")
        
        success = test_career_match(test_case['data'])
        results.append({
            "test_case": test_case['name'],
            "success": success
        })
        
        # Add delay between requests to be respectful to the API
        if i < len(test_cases):
            print("⏳ Waiting 2 seconds before next test...")
            time.sleep(2)
    
    return results

def main():
    """Main test function"""
    print("🚀 CareerMatch Backend Test Suite")
    print("="*50)
    
    # Test 1: Backend Health
    print("\n1. Testing Backend Health...")
    if not test_backend_health():
        print("❌ Backend is not accessible. Please check if the server is running.")
        return
    
    # Test 2: Single Career Match
    print("\n2. Testing Single Career Match...")
    sample_data = {
        "personality": "Outgoing and sociable",
        "weekend": "Spending time with friends and family",
        "solving": "Collaborative and brainstorming-focused",
        "environment": "Collaborative and team-oriented",
        "role": "As a team player, contributing ideas",
        "motivates": "Making a positive impact"
    }
    
    test_career_match(sample_data)
    
    # Test 3: Multiple Personality Types
    print("\n3. Testing Multiple Personality Types...")
    results = test_multiple_personalities()
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 Test Summary")
    print(f"{'='*50}")
    
    successful_tests = sum(1 for result in results if result['success'])
    total_tests = len(results)
    
    print(f"Total Tests: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {total_tests - successful_tests}")
    
    if successful_tests == total_tests:
        print("🎉 All tests passed! Your backend is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check your backend configuration.")
    
    print(f"\nDetailed Results:")
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        print(f"  {result['test_case']}: {status}")

if __name__ == "__main__":
    main() 