'use client';

import * as React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useRouter, useSearchParams } from 'next/navigation';
import { signIn } from '@/lib/auth-client';
import { Input, Button, Checkbox, showToast } from '@/components/ui';
import Link from 'next/link';

const loginSchema = z.object({
    email: z.string().email('Invalid email address'),
    password: z.string().min(1, 'Password is required'),
    rememberMe: z.boolean(),
});

type LoginData = z.infer<typeof loginSchema>;

export function SignInForm() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const returnUrl = searchParams.get('returnUrl') || '/dashboard';
    const [isLoading, setIsLoading] = React.useState(false);

    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<LoginData>({
        resolver: zodResolver(loginSchema),
        defaultValues: {
            email: '',
            password: '',
            rememberMe: false,
        },
    });

    const onSubmit = async (data: LoginData) => {
        setIsLoading(true);
        try {
            const response = await signIn.email({
                email: data.email,
                password: data.password,
                callbackURL: returnUrl,
            });

            if (response?.error) {
                showToast.error(response.error.message || 'Login failed');
            } else {
                showToast.success('Signed in successfully!');
                router.push(returnUrl);
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
                <h2 className="text-3xl font-extrabold text-gray-900">Welcome Back</h2>
                <p className="mt-2 text-sm text-gray-600">
                    Simplify your day, one task at a time.
                </p>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="mt-8 space-y-6">
                <div className="space-y-4">
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
                        {...register('password')}
                    />
                </div>

                <div className="flex items-center justify-between">
                    <Checkbox label="Remember me" {...register('rememberMe')} />
                    <Link
                        href="/forgot-password"
                        className="text-sm font-medium text-emerald-600 hover:text-emerald-500"
                    >
                        Forgot password?
                    </Link>
                </div>

                <Button type="submit" className="w-full py-6 text-lg" isLoading={isLoading}>
                    Sign In
                </Button>

                <p className="text-center text-sm text-gray-600">
                    Don&apos;t have an account?{' '}
                    <Link href="/signup" className="font-bold text-emerald-600 hover:text-emerald-500">
                        Sign Up
                    </Link>
                </p>
            </form>
        </div>
    );
}
