import requests
import time
from datetime import datetime, timedelta
from jose import jwt

# Configuration
BASE_URL = "http://127.0.0.1:8000"
SECRET = "06b431e6430ac5a081311091d76054e5fcaf2db400eabf8ee40dea2f9bd465a7"
ALGORITHM = "HS256"
USER_ID = "test_user_verification"
EMAIL = "verification@example.com"

def create_valid_token():
    expire = datetime.utcnow() + timedelta(days=1)
    to_encode = {
        "sub": USER_ID,
        "email": EMAIL,
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp(),
        "type": "access"
    }
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def test_health():
    print("Checking Health...")
    try:
        res = requests.get(f"{BASE_URL}/health")
        if res.status_code == 200:
            print("✓ Health Check Passed")
            print(res.json())
            return True
        else:
            print(f"✗ Health Check Failed: {res.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health Check Exception: {e}")
        return False

def test_chat():
    print("\nTesting Chat Endpoint...")
    token = create_valid_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    # Note: The actual payload structure depends on Pydantic models in chat.py
    # Accessing common chat payload found in similar apps
    data = {
        "message": "Hello, are you working?",
        "conversation_id": None
    }
    
    url = f"{BASE_URL}/api/{USER_ID}/chat"
    print(f"POST {url}")
    try:
        res = requests.post(url, headers=headers, json=data)
        if res.status_code == 200:
            print("✓ Chat Request Successful")
            print("Response:", res.json())
            return True
        else:
            print(f"✗ Chat Request Failed: {res.status_code}")
            print(res.text)
            return False
    except Exception as e:
        print(f"✗ Chat Request Exception: {e}")
        return False

if __name__ == "__main__":
    if test_health():
        test_chat()
