'use client';

import * as React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useRouter } from 'next/navigation';
import { signUp } from '@/lib/auth-client';
import { Input, Button, Checkbox, showToast } from '@/components/ui';
import Link from 'next/link';

const registerSchema = z.object({
    name: z.string().min(2, 'Name must be at least 2 characters'),
    email: z.string().email('Invalid email address'),
    password: z
        .string()
        .min(8, 'Password must be at least 8 characters')
        .regex(/[A-Z]/, 'Must contain at least one uppercase letter')
        .regex(/[0-9]/, 'Must contain at least one number')
        .regex(/[!@#$%^&*(),.?":{}|<>]/, 'Must contain at least one special character'),
    confirmPassword: z.string(),
    terms: z.literal(true, {
        message: 'You must accept the terms and conditions',
    }),
}).refine((data) => data.password === data.confirmPassword, {
    message: "Passwords don't match",
    path: ['confirmPassword'],
});

type RegisterData = z.infer<typeof registerSchema>;

export function SignUpForm() {
    const router = useRouter();
    const [isLoading, setIsLoading] = React.useState(false);

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<RegisterData>({
        resolver: zodResolver(registerSchema),
    });

    const onSubmit = async (data: RegisterData) => {
        setIsLoading(true);
        try {
            const response = await signUp.email({
                email: data.email,
                password: data.password,
                name: data.name,
                callbackURL: '/dashboard',
            });

            if (response?.error) {
                showToast.error(response.error.message || 'Registration failed');
            } else {
                // Better Auth has created the user and session
                // The backend will verify the JWT token when API requests are made
                showToast.success('Account created! Welcome.');
                router.push('/dashboard');
            }
        } catch {
            showToast.error('An unexpected error occurred');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="w-full max-w-md space-y-8 rounded-3xl border border-gray-100 bg-white p-10 shadow-xl">
            <div className="text-center">
                <h2 className="text-3xl font-extrabold text-gray-900">Get Started</h2>
                <p className="mt-2 text-sm text-gray-600">
                    Create your account and start organizing.
                </p>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="mt-8 space-y-5">
                <Input
                    label="Full Name"
                    placeholder="John Doe"
                    error={errors.name?.message}
                    {...register('name')}
                />
                <Input
                    label="Email Address"
                    type="email"
                    placeholder="name@example.com"
                    error={errors.email?.message}
                    {...register('email')}
                />
                <Input
                    label="Password"
                    type="password"
                    placeholder="••••••••"
                    error={errors.password?.message}
                    helperText="Min 8 chars, 1 uppercase, 1 symbol"
                    {...register('password')}
                />
                <Input
                    label="Confirm Password"
                    type="password"
                    placeholder="••••••••"
                    error={errors.confirmPassword?.message}
                    {...register('confirmPassword')}
                />

                <div className="py-2">
                    <Checkbox
                        label="I agree to the Terms and Conditions"
                        error={errors.terms?.message}
                        {...register('terms')}
                    />
                </div>

                <Button type="submit" className="w-full py-6 text-lg" isLoading={isLoading}>
                    Create Account
                </Button>

                <p className="text-center text-sm text-gray-600">
                    Already have an account?{' '}
                    <Link href="/signin" className="font-bold text-emerald-600 hover:text-emerald-500">
                        Sign In
                    </Link>
                </p>
            </form>
        </div>
    );
}
