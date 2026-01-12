import { betterAuth } from "better-auth";

// Better Auth configuration that connects to our backend API
export const auth = betterAuth({
    secret: process.env.BETTER_AUTH_SECRET || "fallback-test-secret-for-development",
    baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
    emailAndPassword: {
        enabled: true,
        minPasswordLength: 8,
        requireEmailVerification: false
    },
    // Use our API routes to communicate with the backend
    plugins: []
});
