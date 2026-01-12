'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { signOut } from '@/lib/auth-client';
import { api } from '@/lib/api';
import { showToast } from '@/components/ui';

export default function LogoutPage() {
    const router = useRouter();

    useEffect(() => {
        const performLogout = async () => {
            try {
                await Promise.allSettled([
                    signOut(),
                    api.logout()
                ]);
                showToast.success('Logged out successfully');
            } catch (error) {
                console.error('Logout error:', error);
            } finally {
                router.push('/');
            }
        };

        performLogout();
    }, [router]);

    return (
        <div className="flex flex-col items-center justify-center space-y-4">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-emerald-600 border-t-transparent"></div>
            <p className="text-lg font-medium text-gray-600">Signing you out...</p>
        </div>
    );
}
