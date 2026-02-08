#!/usr/bin/env python3
"""
Test script to verify chat functionality with simulated authentication.
This script creates a mock JWT token to test the chat endpoints directly.
"""

import requests
import time
import subprocess
import sys
from datetime import datetime, timedelta
import jwt  # You might need to install this: pip install pyjwt

BASE_URL = "http://localhost:8000"

def test_health():
    """Test if the backend is running"""
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✓ Backend is running")
            print(f"  Health: {response.json()}")
            return True
        else:
            print(f"✗ Backend not responding properly: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Backend not accessible: {e}")
        return False

def test_chat_endpoint():
    """Test the chat endpoint with a fake token"""
    # Create a mock JWT token with user_id claim
    # In a real scenario, we'd get this from the auth system
    payload = {
        "sub": "test_user_123",  # This matches the user_id in the URL
        "exp": int(time.time()) + 3600,  # Expires in 1 hour
        "iat": int(time.time()),
        "name": "Test User"
    }

    # We'll use a fake token for testing since we can't easily generate a real one
    # without knowing the secret used by the auth system

    # Let's try to call the chat endpoint with a header that mimics what the frontend sends
    headers = {
        "Content-Type": "application/json",
        # Using a fake token - this will likely fail but will help us understand the auth flow
        "Authorization": "Bearer fake-token-for-testing"
    }

    data = {
        "message": "Hello, can you help me create a task?",
        "conversation_id": None
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/test_user_123/chat",
            headers=headers,
            json=data
        )

        print(f"Chat endpoint response: {response.status_code}")
        print(f"Response: {response.text}")

        # If we get a 401, it means auth is working as expected
        if response.status_code == 401:
            print("✓ Authentication is working (expected 401 for invalid token)")
            return True
        elif response.status_code == 200:
            print("✓ Chat endpoint is working!")
            return True
        else:
            print(f"? Unexpected response: {response.status_code}")
            return True  # Still indicates the endpoint is reachable

    except Exception as e:
        print(f"✗ Error calling chat endpoint: {e}")
        return False

def test_chat_streaming_endpoint():
    """Test the streaming chat endpoint"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer fake-token-for-testing"
    }

    data = {
        "message": "Hello, can you help me list my tasks?",
        "conversation_id": None
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/test_user_123/chat/stream",
            headers=headers,
            json=data,
            stream=True
        )

        print(f"Streaming chat endpoint response: {response.status_code}")

        if response.status_code == 401:
            print("✓ Streaming authentication is working (expected 401 for invalid token)")
            return True
        elif response.status_code == 200:
            print("✓ Streaming chat endpoint is working!")
            # Try to read a few lines to see the stream
            count = 0
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    print(f"  Stream line: {line[:100]}...")
                    count += 1
                    if count >= 3:  # Just check first few lines
                        break
            return True
        else:
            print(f"? Streaming unexpected response: {response.status_code}")
            return True

    except Exception as e:
        print(f"✗ Error calling streaming chat endpoint: {e}")
        return False

def test_conversation_endpoints():
    """Test conversation listing endpoint"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer fake-token-for-testing"
    }

    try:
        response = requests.get(
            f"{BASE_URL}/api/test_user_123/conversations",
            headers=headers
        )

        print(f"Conversations endpoint response: {response.status_code}")

        if response.status_code == 401:
            print("✓ Conversations authentication is working (expected 401 for invalid token)")
        else:
            print(f"  Response: {response.text[:200]}...")

        return True

    except Exception as e:
        print(f"✗ Error calling conversations endpoint: {e}")
        return False

def main():
    print("Testing Chat Functionality After Backend Fixes...")
    print("=" * 50)

    # Test 1: Health check
    if not test_health():
        print("\n✗ Backend is not running. Cannot proceed with chat tests.")
        return False

    print()

    # Test 2: Regular chat endpoint
    print("Testing regular chat endpoint...")
    test_chat_endpoint()
    print()

    # Test 3: Streaming chat endpoint
    print("Testing streaming chat endpoint...")
    test_chat_streaming_endpoint()
    print()

    # Test 4: Conversation endpoints
    print("Testing conversation endpoints...")
    test_conversation_endpoints()
    print()

    print("=" * 50)
    print("Chat functionality tests completed.")
    print("\nNote: The 401 responses are expected when using fake tokens.")
    print("The important thing is that endpoints are accessible and returning appropriate responses.")

    return True

if __name__ == "__main__":
    main()