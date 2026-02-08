import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=== TESTING STREAMING SERVICE ISSUE ===")

# Test 1: Check environment variables
print("\\n1. Checking environment variables:")
print(f"   OPENROUTER_API_KEY exists: {'OPENROUTER_API_KEY' in os.environ}")
print(f"   OPENROUTER_BASE_URL: {os.getenv('OPENROUTER_BASE_URL', 'NOT SET')}")
print(f"   DEFAULT_MODEL: {os.getenv('DEFAULT_MODEL', 'NOT SET')}")

# Test 2: Try to import and configure settings
print("\\n2. Testing configuration import:")
try:
    from app.config import settings
    print(f"   Settings loaded successfully")
    print(f"   Default model: {settings.default_model}")
    print(f"   OpenRouter API key: {'SET' if settings.openrouter_api_key else 'NOT SET'}")
    print(f"   OpenRouter base URL: {settings.openrouter_base_url}")
except Exception as e:
    print(f"   ERROR loading settings: {e}")

# Test 3: Try to initialize the OpenAI client
print("\\n3. Testing OpenAI client initialization:")
try:
    from app.services.chat_service import get_openai_client
    print("   OpenAI client function imported successfully")

    # Try to get the client (this may fail if API key is invalid)
    client = get_openai_client()
    print("   OpenAI client created successfully")
except Exception as e:
    print(f"   ERROR creating OpenAI client: {e}")

# Test 4: Test if we can import streaming service
print("\\n4. Testing streaming service import:")
try:
    from app.services.streaming_service import StreamingChatService
    print("   StreamingChatService imported successfully")
except Exception as e:
    print(f"   ERROR importing StreamingChatService: {e}")

# Test 5: Test if we can create a basic chat request
print("\\n5. Testing API contract:")
try:
    from app.schemas.api_contract import ChatRequest
    req = ChatRequest(message="test", stream=True)
    print(f"   ChatRequest created: message='{req.message}', stream={req.stream}")
except Exception as e:
    print(f"   ERROR with ChatRequest: {e}")

print("\\n=== TEST COMPLETE ===")