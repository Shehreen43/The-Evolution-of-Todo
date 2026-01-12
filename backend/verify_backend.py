import asyncio
import uuid
import httpx
from app.main import app
from app.database.init_db import create_db_and_tables
from app.database.connection import async_session
from app.models.user import User
from sqlalchemy import select

async def run_verification():
    print("="*80)
    print("STARTING BACKEND VERIFICATION FOR NEON DATABASE & AUTH (ASYNC)")
    print("="*80)

    # 1. Database Setup
    print("\n[STEP 1] Initializing Database...")
    try:
        # We need to run sync init logic in a thread or just hope it works if called directly?
        # create_db_and_tables is SYNC. It uses its own engine.
        await asyncio.to_thread(create_db_and_tables)
        print("[PASS] Database tables initialized successfully.")
    except Exception as e:
        print(f"[FAIL] Database initialization failed: {e}")
        return

    # Generate unique test user data
    unique_id = str(uuid.uuid4())[:8]
    email = f"verify_{unique_id}@example.com"
    password = "SecurePass123!"
    name = f"Verifier {unique_id}"

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        
        # 2. Authentication Flow
        print("\n[STEP 2] Testing Authentication Flow...")
        
        # A. Signup
        print(f"   -> Attempting Signup ({email})...")
        signup_data = {
            "email": email,
            "password": password,
            "name": name
        }
        response = await client.post("/api/auth/signup", json=signup_data)
        if response.status_code == 200:
            print("[PASS] Signup successful.")
            signup_res = response.json()
            user_id = signup_res["user"]["id"]
            token = signup_res["token"]
            print(f"       User ID: {user_id}")
        else:
            print(f"[FAIL] Signup failed: {response.status_code} - {response.text}")
            return

        # B. Signin (Login)
        print("   -> Attempting Signin...")
        login_data = {
            "email": email,
            "password": password
        }
        response = await client.post("/api/auth/signin", json=login_data)
        if response.status_code == 200:
            print("[PASS] Signin successful.")
            login_res = response.json()
            new_token = login_res["token"]
            assert new_token is not None
        else:
            print(f"[FAIL] Signin failed: {response.status_code} - {response.text}")
            return

        auth_headers = {"Authorization": f"Bearer {token}"}

        # C. Verify /me Endpoint
        print("   -> Verifying /api/auth/me...")
        response = await client.get("/api/auth/me", headers=auth_headers)
        if response.status_code == 200:
            print("[PASS] User profile retrieved.")
            assert response.json()["email"] == email
        else:
            print(f"[FAIL] Profile retrieval failed: {response.status_code} - {response.text}")
            return

        # 3. CRUD Operations
        print("\n[STEP 3] Testing Task CRUD Operations...")

        # A. Create Task
        print("   -> Creating a new Task...")
        task_data = {
            "title": "Integration Test Task",
            "description": "Testing CRUD with Neon DB",
            "priority": "high"
        }
        response = await client.post(f"/api/{user_id}/tasks", json=task_data, headers=auth_headers)
        if response.status_code == 201:
            print("[PASS] Task created successfully.")
            created_task = response.json()
            task_id = created_task["id"]
            assert created_task["priority"] == "high"
        else:
            print(f"[FAIL] Task creation failed: {response.status_code} - {response.text}")
            return

        # B. List Tasks (Read)
        print("   -> Listing Tasks...")
        response = await client.get(f"/api/{user_id}/tasks", headers=auth_headers)
        if response.status_code == 200:
            tasks = response.json()
            print(f"[PASS] Retrieved {len(tasks)} tasks.")
            found = any(t["id"] == task_id for t in tasks)
            if not found:
                print("[FAIL] Created task not found in list.")
                return
        else:
            print(f"[FAIL] List tasks failed: {response.status_code} - {response.text}")
            return

        # C. Update Task
        print("   -> Updating Task...")
        update_data = {
            "title": "Updated Integration Task",
            "completed": True
        }
        response = await client.put(f"/api/{user_id}/tasks/{task_id}", json=update_data, headers=auth_headers)
        if response.status_code == 200:
            print("[PASS] Task updated successfully.")
            updated_task = response.json()
            assert updated_task["title"] == "Updated Integration Task"
        else:
            print(f"[FAIL] Task update failed: {response.status_code} - {response.text}")
            return

        # D. Delete Task
        print("   -> Deleting Task...")
        response = await client.delete(f"/api/{user_id}/tasks/{task_id}", headers=auth_headers)
        if response.status_code == 204:
            print("[PASS] Task deleted successfully.")
        else:
            print(f"[FAIL] Task delete failed: {response.status_code} - {response.text}")
            return

    # 4. Database Persistence Check
    print("\n[STEP 4] Verifying Data Persistence in Neon DB...")
    # Use sync engine for verification to be totally safe? 
    # Or use async_session since we are in async loop?
    # Let's use async_session to show off async capability.
    
    try:
        async with async_session() as session:
            stmt = select(User).where(User.email == email)
            result = await session.execute(stmt)
            user_db = result.scalars().first()
            
            if user_db:
                print(f"[PASS] User '{email}' confirmed in Neon Database.")
                db_verified = True
            else:
                print(f"[FAIL] User '{email}' NOT found in Database!")
                db_verified = False
                
    except Exception as e:
        print(f"[FAIL] Database persistence check failed: {e}")
        db_verified = False

    if db_verified:
        print("\n" + "="*80)
        print("VERIFICATION COMPLETE: BACKEND IS READY FOR FRONTEND INTEGRATION")
        print("="*80)
    else:
        print("\n[FAIL] Verification incomplete.")

if __name__ == "__main__":
    if asyncio.get_event_loop().is_closed():
        asyncio.run(run_verification())
    else:
        # For environments where loop is already running
        try:
            asyncio.run(run_verification())
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(run_verification())
