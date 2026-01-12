import { NextRequest } from "next/server";
import { NextResponse } from "next/server";

// Bridge API route to forward auth requests to backend
export async function GET(
  request: NextRequest,
  { params }: { params: { auth: string[] } }
) {
  try {
    const backendUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/auth/${params.auth.join('/')}`;
    const response = await fetch(backendUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...Object.fromEntries(request.headers.entries()), // Forward all headers
      },
    });

    const data = await response.json();

    // Create response with proper session handling
    const nextResponse = NextResponse.json(data, { status: response.status });

    // If this is a session-related response, set appropriate cookies
    if (response.status === 200 && params.auth[0] === 'me' && data.id) {
      // For user profile requests, we don't need to set a cookie but we can verify the session
    }

    return nextResponse;
  } catch (error) {
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

export async function POST(
  request: NextRequest,
  { params }: { params: { auth: string[] } }
) {
  try {
    const backendUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/auth/${params.auth.join('/')}`;
    const body = await request.json();

    const response = await fetch(backendUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...Object.fromEntries(request.headers.entries()), // Forward all headers
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();

    // Create response with proper session handling
    const nextResponse = NextResponse.json(data, { status: response.status });

    // Set cookies if this is a login/signup response
    if (response.status === 200 && (params.auth[0] === 'signin' || params.auth[0] === 'signup')) {
      if (data.token) {
        // Set the token as a cookie for middleware compatibility
        nextResponse.cookies.set('better_auth_token', data.token, {
          httpOnly: true,
          secure: process.env.NODE_ENV === 'production',
          maxAge: 60 * 60 * 24 * 7, // 1 week
          path: '/',
          sameSite: 'strict',
        });
      }
    } else if (params.auth[0] === 'logout') {
      // Clear the cookie on logout
      nextResponse.cookies.set('better_auth_token', '', {
        httpOnly: true,
        maxAge: 0, // Expire immediately
        path: '/',
      });
    }

    return nextResponse;
  } catch (error) {
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}