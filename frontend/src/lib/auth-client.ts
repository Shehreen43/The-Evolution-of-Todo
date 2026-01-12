"use client";

// Custom auth client that directly communicates with backend API
import { useState, useEffect } from 'react';

// Define types
interface User {
  id: string;
  email: string;
  name: string;
}

interface TokenResponse {
  user: User;
  token: string;
  expires_at: string;
}

// Simple auth client implementation that calls backend directly
const createSimpleAuthClient = () => {
  const signUp = {
    email: async (data: { email: string; password: string; name: string; callbackURL?: string }) => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/signup`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: data.email,
            password: data.password,
            name: data.name
          }),
        });

        const result = await response.json();

        if (response.ok) {
          // Store token in localStorage and cookies for consistency
          if (result.token) {
            localStorage.setItem('better_auth_token', result.token);
            // Also set in cookies for middleware compatibility
            document.cookie = `better_auth_token=${result.token}; path=/; max-age=604800`; // 7 days
          }
          return { data: result, error: null };
        } else {
          return { data: null, error: { message: result.detail || 'Signup failed' } };
        }
      } catch (error) {
        return { data: null, error: { message: 'Network error occurred' } };
      }
    }
  };

  const signIn = {
    email: async (data: { email: string; password: string; callbackURL?: string }) => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/signin`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: data.email,
            password: data.password
          }),
        });

        const result = await response.json();

        if (response.ok) {
          // Store token in localStorage and cookies for consistency
          if (result.token) {
            localStorage.setItem('better_auth_token', result.token);
            // Also set in cookies for middleware compatibility
            document.cookie = `better_auth_token=${result.token}; path=/; max-age=604800`; // 7 days
          }
          return { data: result, error: null };
        } else {
          return { data: null, error: { message: result.detail || 'Login failed' } };
        }
      } catch (error) {
        return { data: null, error: { message: 'Network error occurred' } };
      }
    }
  };

  const signOut = async () => {
    try {
      await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/logout`, {
        method: 'POST',
      });

      // Remove token from localStorage and cookies
      localStorage.removeItem('better_auth_token');
      document.cookie = 'better_auth_token=; path=/; max-age=0'; // Expire the cookie
      return { error: null };
    } catch (error) {
      return { error: { message: 'Network error occurred' } };
    }
  };

  const useSession = () => {
    const [session, setSession] = useState<{ data?: { user: User }; isPending: boolean }>({ isPending: true });

    useEffect(() => {
      const fetchSession = async () => {
        try {
          const token = localStorage.getItem('better_auth_token');
          if (!token) {
            setSession({ isPending: false });
            return;
          }

          const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/auth/me`, {
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          });

          if (response.ok) {
            const user = await response.json();
            setSession({ data: { user }, isPending: false });
          } else {
            setSession({ isPending: false });
          }
        } catch (error) {
          setSession({ isPending: false });
        }
      };

      fetchSession();
    }, []);

    return session;
  };

  return { signUp, signIn, signOut, useSession };
};

export const {
  signUp,
  signIn,
  signOut,
  useSession,
} = createSimpleAuthClient();
