import httpx
import asyncio
import json
import sys
import os
from datetime import datetime

BASE_URL = "http://localhost:8000"
TEST_USER = {
    "email": f"chat_crud_test_{int(datetime.now().timestamp())}@example.com",
    "password": "TestPassword123!",
    "name": "Chat CRUD Tester"
}

async def verify_everything():
    print("="*80)
    print("STARTING COMPREHENSIVE CHAT & CRUD VERIFICATION")
    print("="*80)

    async with httpx.AsyncClient(timeout=60.0) as client:
        # 1. Signup
        print("\n[STEP 1] Creating test user...")
        try:
            resp = await client.post(f"{BASE_URL}/api/auth/signup", json=TEST_USER)
            if resp.status_code == 200:
                data = resp.json()
                token = data["token"]
                user_id = data["user"]["id"]
                print(f"[PASS] User created with ID: {user_id}")
            else:
                print(f"[FAIL] Signup failed: {resp.status_code} - {resp.text}")
                return
        except Exception as e:
            print(f"[FAIL] Signup exception: {e}")
            return

        await asyncio.sleep(3)
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Test Standard Chat
        print("\n[STEP 2] Testing Standard Chat...")
        try:
            resp = await client.post(
                f"{BASE_URL}/api/{user_id}/chat",
                headers=headers,
                json={"message": "Hello! Can you help me manage my tasks?"}
            )
            if resp.status_code == 200:
                chat_data = resp.json()
                print(f"[PASS] Standard chat succeeded.")
                print(f"       AI Response: {chat_data.get('response')[:100]}...")
            else:
                print(f"[FAIL] Standard chat failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"[FAIL] Standard chat exception: {e}")

        await asyncio.sleep(5)

        # 3. Test Streaming Chat
        print("\n[STEP 3] Testing Streaming Chat...")
        try:
            async with client.stream(
                "POST",
                f"{BASE_URL}/api/{user_id}/chat/stream",
                headers=headers,
                json={"message": "Tell me a very short joke."}
            ) as response:
                if response.status_code == 200:
                    print(f"[PASS] Streaming connection established.")
                    print("       Chunks: ", end="", flush=True)
                    full_response = ""
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            try:
                                event = json.loads(line[6:])
                                if event["type"] == "token":
                                    content = event["data"]["content"]
                                    print(content, end="", flush=True)
                                    full_response += content
                                elif event["type"] == "error":
                                    print(f"\n[FAIL] Stream error: {event['data']['error']}")
                            except:
                                pass
                    print(f"\n[DONE] Stream finished. Length: {len(full_response)} chars.")
                else:
                    print(f"[FAIL] Streaming failed: {response.status_code}")
        except Exception as e:
            print(f"[FAIL] Streaming exception: {e}")

        await asyncio.sleep(5)

        # 4. CRUD via Chat: Create Task
        print("\n[STEP 4] CRUD via Chat: Creating a task...")
        task_title = f"Test Task {int(datetime.now().timestamp())}"
        try:
            resp = await client.post(
                f"{BASE_URL}/api/{user_id}/chat",
                headers=headers,
                json={"message": f"Please add a high priority task titled '{task_title}' with description 'Verified via script'."}
            )
            if resp.status_code == 200:
                print(f"[PASS] Chat request to create task sent.")
                # Verify task exists in DB via API
                tasks_resp = await client.get(f"{BASE_URL}/api/{user_id}/tasks", headers=headers)
                if tasks_resp.status_code == 200:
                    tasks = tasks_resp.json()
                    found = [t for t in tasks if t["title"] == task_title]
                    if found:
                        task_id = found[0]["id"]
                        print(f"[PASS] Task verified in database. ID: {task_id}")
                    else:
                        print(f"[FAIL] Task '{task_title}' not found in database after chat command.")
                        return
                else:
                    print(f"[FAIL] Failed to list tasks for verification: {tasks_resp.status_code}")
                    return
            else:
                print(f"[FAIL] Chat request failed: {resp.status_code} - {resp.text}")
                return
        except Exception as e:
            print(f"[FAIL] Chat CRUD exception: {e}")
            return

        await asyncio.sleep(5)

        # 5. CRUD via Chat: Update Task
        print("\n[STEP 5] CRUD via Chat: Updating the task...")
        try:
            resp = await client.post(
                f"{BASE_URL}/api/{user_id}/chat",
                headers=headers,
                json={"message": f"Mark the task '{task_title}' as completed."}
            )
            if resp.status_code == 200:
                print(f"[PASS] Chat request to update task sent.")
                # Verify update
                task_resp = await client.get(f"{BASE_URL}/api/{user_id}/tasks/{task_id}", headers=headers)
                if task_resp.status_code == 200:
                    task = task_resp.json()
                    if task.get("completed"):
                        print(f"[PASS] Task completion verified in database.")
                    else:
                        print(f"[FAIL] Task still not completed in database.")
                else:
                    print(f"[FAIL] Failed to get task for verification: {task_resp.status_code}")
            else:
                print(f"[FAIL] Chat update request failed: {resp.status_code}")
        except Exception as e:
            print(f"[FAIL] Chat update exception: {e}")

        # 6. CRUD via Chat: Delete Task
        print("\n[STEP 6] CRUD via Chat: Deleting the task...")
        try:
            resp = await client.post(
                f"{BASE_URL}/api/{user_id}/chat",
                headers=headers,
                json={"message": f"Delete the task titled '{task_title}'."}
            )
            if resp.status_code == 200:
                print(f"[PASS] Chat request to delete task sent.")
                # Verify deletion
                task_resp = await client.get(f"{BASE_URL}/api/{user_id}/tasks/{task_id}", headers=headers)
                if task_resp.status_code == 404:
                    print(f"[PASS] Task deletion verified. 404 Returned.")
                else:
                    print(f"[FAIL] Task still exists or returned status {task_resp.status_code}")
            else:
                print(f"[FAIL] Chat delete request failed: {resp.status_code}")
        except Exception as e:
            print(f"[FAIL] Chat delete exception: {e}")

    print("\n" + "="*80)
    print("COMPREHENSIVE VERIFICATION COMPLETE")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(verify_everything())
