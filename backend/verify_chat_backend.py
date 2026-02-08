import httpx
import asyncio
import json
import sys

BASE_URL = "http://localhost:8000"
TEST_USER = {
    "email": "chat_tester@example.com",
    "password": "ChatPassword123!",
    "name": "Chat Tester"
}

async def verify_chat():
    print("="*80)
    print("STARTING CHAT BACKEND VERIFICATION")
    print("="*80)

    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Auth - Try Signin first, then Signup
        print("\n[STEP 1] Authenticating...")
        try:
            resp = await client.post(f"{BASE_URL}/api/auth/signin", json={
                "email": TEST_USER["email"],
                "password": TEST_USER["password"]
            })
            if resp.status_code != 200:
                print("Signin failed, trying signup...")
                resp = await client.post(f"{BASE_URL}/api/auth/signup", json=TEST_USER)
                
            if resp.status_code == 200:
                data = resp.json()
                token = data["token"]
                user_id = data["user"]["id"]
                print(f"[PASS] Authenticated as {user_id}")
            else:
                print(f"[FAIL] Auth failed: {resp.status_code} - {resp.text}")
                return
        except Exception as e:
            print(f"[FAIL] Auth exception: {e}")
            return

        headers = {"Authorization": f"Bearer {token}"}

        # 2. Test Standard Chat
        print("\n[STEP 2] Testing Standard Chat (/api/{user_id}/chat)...")
        try:
            resp = await client.post(
                f"{BASE_URL}/api/{user_id}/chat",
                headers=headers,
                json={"message": "Respond with 'BACKEND_OK_CHATBOT' if you can read this."}
            )
            if resp.status_code == 200:
                chat_data = resp.json()
                print(f"[PASS] Standard chat succeeded.")
                print(f"       AI Response: {chat_data.get('response')}")
            else:
                print(f"[FAIL] Standard chat failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"[FAIL] Standard chat exception: {e}")

        # 3. Test Streaming Chat
        print("\n[STEP 3] Testing Streaming Chat (/api/{user_id}/chat/stream)...")
        try:
            async with client.stream(
                "POST",
                f"{BASE_URL}/api/{user_id}/chat/stream",
                headers=headers,
                json={"message": "Respond with 'STREAM_OK'."}
            ) as response:
                if response.status_code == 200:
                    print(f"[PASS] Streaming connection established.")
                    print("       Chunks: ", end="", flush=True)
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            try:
                                event = json.loads(line[6:])
                                if event["type"] == "token":
                                    print(event["data"]["content"], end="", flush=True)
                                elif event["type"] == "error":
                                    print(f"\n[FAIL] Stream error: {event['data']['error']}")
                            except:
                                pass
                    print("\n[DONE] Stream finished.")
                else:
                    print(f"[FAIL] Streaming failed: {response.status_code}")
        except Exception as e:
            print(f"[FAIL] Streaming exception: {e}")

if __name__ == "__main__":
    asyncio.run(verify_chat())
