# Feature: User Authentication & Authorization with Better Auth

This document defines the User Authentication & Authorization feature for Phase II of "The Evolution of Todo" project, implementing Better Auth for secure user identity management.

## Overview

| Attribute | Value |
|-----------|-------|
| **Feature ID** | authentication |
| **Priority** | P1 (Must Have) |
| **Phase** | Phase II (Full-Stack Web) |
| **Dependencies** | None (foundational) |
| **Status** | Draft |

---

## Feature Overview

- Authentication system using Better Auth
- JWT token-based authorization
- User session management

---

## User Stories

### US-AUTH-001: Sign Up

> **As a** new user,
> **I can** sign up with email and password,
> **So that** I can create a personal account to manage my tasks.

**Acceptance Criteria:**
- [ ] Email validation (proper format)
- [ ] Password requirements (min 8 chars, 1 uppercase, 1 number)
- [ ] Password confirmation match
- [ ] Create user record in database
- [ ] Auto sign-in after successful signup

---

### US-AUTH-002: Sign In

> **As a** returning user,
> **I can** sign in with my credentials,
> **So that** I can access my personal task list.

**Acceptance Criteria:**
- [ ] Email and password validation
- [ ] Verify credentials against database
- [ ] Generate JWT token on success
- [ ] Store token securely in httpOnly cookie
- [ ] Redirect to dashboard

---

### US-AUTH-003: Sign Out

> **As an** authenticated user,
> **I can** sign out,
> **So that** I can prevent unauthorized access on shared devices.

**Acceptance Criteria:**
- [ ] Clear JWT token from cookies
- [ ] Clear frontend auth state
- [ ] Redirect to login page

---

### US-AUTH-004: Session Persistence

> **As a** user,
> **My session** persists across browser refreshes,
> **So that** I don't need to log in repeatedly.

**Acceptance Criteria:**
- [ ] Check for valid JWT on app load
- [ ] Refresh token before expiry (7 days default)
- [ ] Auto logout on token expiration

---

## Authentication Flow

### Sign Up Flow

**Sign Up Steps:**
1. User fills signup form (email, password, confirm password)
2. Frontend validates email format
3. Frontend validates password requirements (min 8 chars, 1 uppercase, 1 number)
4. Frontend validates password confirmation match
5. API call to create user account
6. Backend checks email uniqueness
7. Password hashed (handled by Better Auth with bcrypt)
8. User record created in database
9. Auto sign-in after successful signup
10. JWT token generated and stored in httpOnly cookie
11. Redirect to dashboard

---

### Sign In Flow

**Sign In Steps:**
1. User fills login form (email, password)
2. Email and password validation on frontend
3. API call to authenticate
4. Backend validates credentials against database
5. Generate JWT token on success
6. Store token securely in httpOnly cookie
7. Redirect to dashboard

---

### Sign Out Flow

**Sign Out Steps:**
1. User clicks logout button
2. Clear JWT token from cookies
3. Clear frontend auth state
4. Redirect to login page

---

### Session Management Flow

**Session Management Steps:**
1. Check for valid JWT on app load
2. Verify token validity and expiration
3. Refresh token 1 day before expiry
4. Auto logout on token expiration
5. Maintain session state across browser refreshes

---

## JWT Token Structure

### Token Payload

```json
{
  "user_id": "user-uuid-here",
  "email": "user@example.com",
  "iat": 1704067200,
  "expires_at": 1704672000
}
```

### Claims Description

| Claim | Type | Description |
|-------|------|-------------|
| `user_id` | string | User ID (subject of the token) |
| `email` | string | User's email address |
| `iat` | integer | Issued at timestamp (Unix epoch) |
| `expires_at` | integer | Expiration timestamp (Unix epoch) |

### Token Configuration

- **Signature**: HMAC-SHA256 with BETTER_AUTH_SECRET
- **Expiry**: 7 days
- **Refresh**: 1 day before expiry

---

## Security Requirements

### HTTPS Configuration
- **Production**: HTTPS only in production
- **Development**: HTTP allowed for local development

### Cookie Security
- **httpOnly**: Cookies set to httpOnly (prevent XSS)
- **Secure**: Secure flag set in production
- **SameSite**: Strict mode for CSRF protection

### Password Security
- **Hashing**: Password hashing with bcrypt
- **Requirements**: Min 8 chars, 1 uppercase, 1 number
- **Validation**: Client and server-side validation

### Rate Limiting
- **Auth Endpoints**: Rate limiting on auth endpoints (5 attempts per 15 min)
- **IP-based**: Limit requests per IP address
- **Account Lockout**: Temporary lockout after failed attempts

### Environment Variables

#### Frontend (.env.local)
```env
# Frontend environment variables
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-32-character-secret-key-here
DATABASE_URL=postgresql+asyncpg://user:password@host/db
```

#### Backend (.env)
```env
# Backend environment variables
DATABASE_URL=postgresql+asyncpg://user:password@host/db
BETTER_AUTH_SECRET=your-32-character-secret-key-here
ALGORITHM=HS256
```

### Security Controls

| Control | Implementation |
|---------|----------------|
| **HTTPS** | All traffic encrypted in production |
| **Password Hashing** | bcrypt (handled by Better Auth) |
| **JWT Signing** | HS256 with shared secret |
| **Token Expiration** | 7 days (604800 seconds) |
| **User Isolation** | All queries filtered by user_id |
| **CORS** | Whitelist frontend origins only |
| **Secret Management** | Environment variables only |
| **CSRF Protection** | Built-in with Better Auth |

---

## Backend Integration

### JWT Verification Middleware

```python
# backend/app/api/deps.py
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel

# Security scheme
security = HTTPBearer()

# JWT settings (must match Better Auth config)
BETTER_AUTH_SECRET = "your-shared-secret-key"  # From environment variable
ALGORITHM = "HS256"

class TokenPayload(BaseModel):
    user_id: str      # User ID from Better Auth
    email: str        # User email from Better Auth
    issued_at: int    # Issued at timestamp
    expires_at: int   # Expiration timestamp

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenPayload:
    """Verify JWT and extract user information."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT token
        payload = jwt.decode(
            credentials.credentials,
            BETTER_AUTH_SECRET,
            algorithms=[ALGORITHM]
        )

        # Extract required claims
        user_id: str = payload.get("user_id")
        email: str = payload.get("email")

        if user_id is None or email is None:
            raise credentials_exception

        return TokenPayload(
            user_id=user_id,
            email=email,
            issued_at=payload.get("issued_at", 0),
            expires_at=payload.get("expires_at", 0)
        )

    except JWTError:
        raise credentials_exception
```

### User Isolation Implementation

```python
# backend/app/api/deps.py
from fastapi import HTTPException, status, Depends
from .deps import get_current_user, TokenPayload

async def verify_user_access(
    user_id: str,
    current_user: TokenPayload = Depends(get_current_user)
) -> str:
    """
    Verify that the authenticated user has access to the requested resource.
    Returns the user_id if access is granted.
    """
    # Extract user_id from JWT token
    token_user_id = current_user.user_id

    # Check if the token user matches the requested user
    if user_id != token_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Invalid or expired token"
        )

    return user_id
```

---

## Frontend Integration

### Better Auth Configuration

```typescript
// frontend/lib/auth.ts
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: process.env.DATABASE_URL,
  secret: process.env.BETTER_AUTH_SECRET,
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
    minPasswordLength: 8,
  },
  session: {
    expiresIn: 7 * 24 * 60 * 60, // 7 days in seconds
    updateAge: 24 * 60 * 60,     // Update session every 24 hours
  },
  cookies: {
    secure: process.env.NODE_ENV === "production",
    sameSite: "strict",
  },
  plugins: [
    // JWT plugin for token-based authentication
    {
      id: "jwt",
      init: (ctx) => {
        return {
          // Token configuration
          token: {
            expiration: 7 * 24 * 60 * 60 * 1000, // 7 days in milliseconds
          },
        }
      },
    },
  ],
});
```

### API Client with JWT Integration

```typescript
// frontend/lib/api-client.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiClient {
  private async getAuthHeaders(): Promise<Record<string, string>> {
    // Get JWT from Better Auth session
    const session = await auth.getSession();
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };

    if (session?.token) {
      headers["Authorization"] = `Bearer ${session.token}`;
    }

    return headers;
  }

  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers = await this.getAuthHeaders();

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        ...headers,
        ...options.headers,
      },
    });

    if (response.status === 401) {
      // Token expired or invalid - redirect to login
      window.location.href = "/signin";
      throw new Error("Session expired");
    }

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Request failed");
    }

    return response.json();
  }
}

export const api = new ApiClient();
```

### Auth Context Provider

```typescript
// frontend/contexts/AuthContext.tsx
import React, { createContext, useContext, useEffect, useState } from 'react';
import { useAuth } from 'better-auth/react';

interface AuthContextType {
  user: any;
  isAuthenticated: boolean;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { session, signIn, signOut, user } = useAuth();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check initial session status
    setIsLoading(!session);
  }, [session]);

  const value = {
    user: user,
    isAuthenticated: !!session,
    isLoading: isLoading,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuthContext = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuthContext must be used within an AuthProvider');
  }
  return context;
};
```

---

## Error Handling

### Authentication Errors

| Error Type | Message | Status Code |
|------------|---------|-------------|
| Invalid Credentials | "Email or password incorrect" | 401 |
| Email Already Exists | "Email already exists" | 409 |
| Invalid Email Format | "Invalid email format" | 400 |
| Weak Password | "Password must meet requirements" | 400 |
| Password Mismatch | "Passwords do not match" | 400 |
| Expired Token | "Session expired" | 401 |
| Invalid Token | "Invalid session" | 401 |

### API Error Handling

```typescript
// frontend/lib/error-handling.ts
export const handleAuthError = (error: any): string => {
  const message = error.message || "An error occurred";

  if (message.includes("Email or password")) {
    return "Email or password incorrect";
  }

  if (message.includes("Email already")) {
    return "Email already exists";
  }

  if (message.includes("Session expired")) {
    // Redirect to login handled by API client
    return "Session expired";
  }

  return message;
};
```

---

## Database Schema

### Users Table (Managed by Better Auth)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | str | PK, max 255 | Unique user ID (UUID) |
| email | str | UK, max 255 | Email address (unique) |
| name | str | max 255 | Display name |
| password | str | - | Hashed password (bcrypt) |
| email_verified | boolean | - | Email verification status |
| created_at | datetime | auto | Creation timestamp |
| updated_at | datetime | auto | Last update timestamp |

### Sessions Table (Better Auth)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | str | PK | Session ID |
| user_id | str | FK | Reference to user |
| token | str | - | JWT token |
| expires_at | datetime | - | Token expiration |
| created_at | datetime | auto | Creation timestamp |

---

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create new user account |
| POST | `/api/auth/login` | Authenticate and get JWT |
| POST | `/api/auth/logout` | Sign out (clear session) |
| GET | `/api/auth/me` | Get current user info |

### Protected Endpoints (Require JWT)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

---

## UI Requirements

### Login Page

| Element | Requirement |
|---------|-------------|
| Email input | Required, email validation |
| Password input | Required, masked characters |
| Sign In button | Primary action |
| Sign Up link | Navigate to signup page |
| Error messages | Visible, specific |
| Loading state | Show spinner while processing |

### Signup Page

| Element | Requirement |
|---------|-------------|
| Email input | Required, email validation |
| Password input | Required, show requirements |
| Confirm password | Required, must match primary password |
| Name input | Optional |
| Sign Up button | Primary action |
| Sign In link | Navigate to login page |
| Password strength | Visual indicator |
| Error messages | Visible, specific |

### Authenticated Layout

| Element | Requirement |
|---------|-------------|
| User name/avatar | Display in header |
| Logout button | Visible, accessible |
| Protected routes | Redirect if not authenticated |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Login success rate | > 98% | Auth logs |
| Signup conversion | > 50% | Analytics |
| Session duration | > 5 days average | Session data |
| Failed login rate | < 2% | Auth logs |
| Unauthorized access blocked | 100% | Security logs |

---

## Related Documents

| Document | Path | Purpose |
|----------|------|---------|
| Architecture | `architecture.md` | System architecture |
| API Spec | `api/rest-endpoints.md` | Endpoint details |
| Database Schema | `database/schema.md` | Table definitions |
| Task CRUD | `features/task-crud.md` | Task operations |

---

## Version Information

| Item | Value |
|------|-------|
| Feature | User Authentication & Authorization |
| Version | 2.0.0 |
| Status | Draft |
| Last Updated | 2026-01-09 |