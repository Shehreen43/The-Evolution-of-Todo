import httpx
import asyncio
import json

BASE_URL = "http://localhost:8000"
TEST_USER = {
    "email": f"crud_test_{int(asyncio.get_event_loop().time())}@example.com",
    "password": "CrudPassword123!",
    "name": "CRUD Tester"
}

async def verify_crud():
    print("="*80)
    print("STARTING CRUD OPERATIONS VERIFICATION")
    print("="*80)

    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Signup/Signin
        print("\n[STEP 1] Authenticating...")
        try:
            resp = await client.post(f"{BASE_URL}/api/auth/signup", json=TEST_USER)
            if resp.status_code != 200:
                print(f"[FAIL] Signup failed: {resp.status_code} - {resp.text}")
                return
            
            data = resp.json()
            token = data["token"]
            user_id = data["user"]["id"]
            print(f"[PASS] Authenticated as {user_id}")
        except Exception as e:
            print(f"[FAIL] Auth exception: {e}")
            return

        headers = {"Authorization": f"Bearer {token}"}

        # 2. Create Task
        print("\n[STEP 2] Creating Task...")
        task_data = {
            "title": "CRUD Test Task",
            "description": "Verification of task creation",
            "priority": "high"
        }
        try:
            resp = await client.post(f"{BASE_URL}/api/{user_id}/tasks", headers=headers, json=task_data)
            if resp.status_code == 201 or resp.status_code == 200:
                task = resp.json()
                task_id = task["id"]
                print(f"[PASS] Task created with ID: {task_id}")
            else:
                print(f"[FAIL] Task creation failed: {resp.status_code} - {resp.text}")
                return
        except Exception as e:
            print(f"[FAIL] Task creation exception: {e}")
            return

        # 3. List Tasks
        print("\n[STEP 3] Listing Tasks...")
        try:
            resp = await client.get(f"{BASE_URL}/api/{user_id}/tasks", headers=headers)
            if resp.status_code == 200:
                tasks = resp.json()
                found = any(t["id"] == task_id for t in tasks)
                if found:
                    print(f"[PASS] Task {task_id} found in list. Total tasks: {len(tasks)}")
                else:
                    print(f"[FAIL] Task {task_id} not found in list.")
            else:
                print(f"[FAIL] List tasks failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"[FAIL] List tasks exception: {e}")

        # 4. Update Task
        print("\n[STEP 4] Updating Task...")
        update_data = {"completed": True, "title": "Updated CRUD Task"}
        try:
            # Check if PATCH or PUT is used. Based on tasks.py, both might exist.
            # Using PUT as defined in CLAUDE.md guidelines
            resp = await client.put(f"{BASE_URL}/api/{user_id}/tasks/{task_id}", headers=headers, json=update_data)
            if resp.status_code == 200:
                updated_task = resp.json()
                if updated_task["completed"] == True:
                    print(f"[PASS] Task {task_id} updated successfully.")
                else:
                    print(f"[FAIL] Task updated but status mismatch.")
            else:
                print(f"[FAIL] Task update failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"[FAIL] Task update exception: {e}")

        # 5. Delete Task
        print("\n[STEP 5] Deleting Task...")
        try:
            resp = await client.delete(f"{BASE_URL}/api/{user_id}/tasks/{task_id}", headers=headers)
            if resp.status_code in [200, 204]:
                print(f"[PASS] Task {task_id} deleted successfully.")
            else:
                print(f"[FAIL] Task deletion failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"[FAIL] Task deletion exception: {e}")

        # 6. Verify Deletion
        print("\n[STEP 6] Verifying Deletion...")
        try:
            resp = await client.get(f"{BASE_URL}/api/{user_id}/tasks/{task_id}", headers=headers)
            if resp.status_code == 404:
                print("[PASS] Task definitely gone.")
            else:
                print(f"[FAIL] Task still exists or unexpected status: {resp.status_code}")
        except Exception as e:
            print(f"[FAIL] Verification exception: {e}")

    print("\n" + "="*80)
    print("CRUD VERIFICATION COMPLETE")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(verify_crud())
