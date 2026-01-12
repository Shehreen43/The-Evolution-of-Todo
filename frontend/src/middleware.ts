import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
    // Check for Better Auth session token in cookies
    // Better Auth typically sets session cookies with patterns like:
    // 'better-auth.session_token' or similar
    const { pathname } = request.nextUrl;

    // Protected routes
    const protectedRoutes = ["/dashboard", "/profile", "/tasks"];
    const isProtectedRoute = protectedRoutes.some(route => pathname.startsWith(route));

    // Auth routes (redirect to dashboard if already logged in)
    const authRoutes = ["/signin", "/signup"];
    const isAuthRoute = authRoutes.some(route => pathname.startsWith(route));

    // Check for Better Auth session by looking for Better Auth specific cookies
    // Better Auth typically sets cookies like 'better-auth.session_token' or our custom token
    const hasBetterAuthSession = request.cookies.getAll().some(cookie =>
        cookie.name.includes('better-auth.session_token') ||
        cookie.name.includes('better-auth.') ||
        cookie.name === 'better_auth_token'
    );

    if (isProtectedRoute && !hasBetterAuthSession) {
        const url = new URL("/signin", request.url);
        url.searchParams.set("returnUrl", pathname);
        return NextResponse.redirect(url);
    }

    if (isAuthRoute && hasBetterAuthSession) {
        return NextResponse.redirect(new URL("/dashboard", request.url));
    }

    return NextResponse.next();
}

export const config = {
    matcher: ["/dashboard/:path*", "/profile/:path*", "/tasks/:path*", "/signin", "/signup"],
};
