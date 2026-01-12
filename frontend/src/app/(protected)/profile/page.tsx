'use client';

import * as React from 'react';
import { useSession, signOut } from '@/lib/auth-client';
import { PageHeader } from '@/components/layout/page-layouts';
import { Button, Input, showToast } from '@/components/ui';
import { api } from '@/lib/api';
import { User, Mail, Calendar, Shield, LogOut } from 'lucide-react';

export default function ProfilePage() {
    const { data: session } = useSession();

    const handleLogout = async () => {
        try {
            await signOut();
            await api.logout();
            showToast.success('Signed out');
        } catch {
            showToast.error('Logout failed');
        }
    };

    if (!session?.user) return null;

    return (
        <div className="max-w-4xl space-y-8">
            <PageHeader title="My Profile" description="Manage your account settings and preferences." />

            {/* Profile Card */}
            <div className="overflow-hidden rounded-[2rem] border border-gray-100 bg-white shadow-xl">
                <div className="h-32 bg-emerald-600" />
                <div className="relative px-8 pb-8">
                    <div className="absolute -top-12 flex h-24 w-24 items-center justify-center rounded-3xl bg-white p-1 shadow-lg">
                        <div className="flex h-full w-full items-center justify-center rounded-2xl bg-emerald-100 text-3xl font-black text-emerald-700">
                            {session.user.name?.[0] || 'U'}
                        </div>
                    </div>

                    <div className="pt-16">
                        <h2 className="text-2xl font-bold text-gray-900">{session.user.name}</h2>
                        <p className="text-gray-500">{session.user.email}</p>
                    </div>

                    <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2">
                        <div className="flex items-center gap-4 rounded-2xl border border-gray-50 bg-gray-50/50 p-4">
                            <Mail className="h-5 w-5 text-emerald-600" />
                            <div>
                                <p className="text-xs font-bold uppercase tracking-wider text-gray-400">Email Address</p>
                                <p className="text-sm font-medium text-gray-900">{session.user.email}</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-4 rounded-2xl border border-gray-50 bg-gray-50/50 p-4">
                            <Calendar className="h-5 w-5 text-emerald-600" />
                            <div>
                                <p className="text-xs font-bold uppercase tracking-wider text-gray-400">Member Since</p>
                                <p className="text-sm font-medium text-gray-900">January 2026</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Settings Groups */}
            <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
                <section className="space-y-4 rounded-[2rem] border border-gray-100 bg-white p-8">
                    <h3 className="flex items-center gap-2 text-lg font-bold text-gray-900">
                        <User className="h-5 w-5 text-emerald-600" />
                        Personal Info
                    </h3>
                    <Input label="Display Name" defaultValue={session.user.name} />
                    <Button variant="outline" className="w-full">Update Name</Button>
                </section>

                <section className="space-y-4 rounded-[2rem] border border-gray-100 bg-white p-8">
                    <h3 className="flex items-center gap-2 text-lg font-bold text-gray-900">
                        <Shield className="h-5 w-5 text-emerald-600" />
                        Security
                    </h3>
                    <p className="text-sm text-gray-500">Change your password or manage active sessions.</p>
                    <Button variant="outline" className="w-full">Change Password</Button>
                </section>
            </div>

            <div className="flex justify-center pt-8">
                <Button
                    variant="ghost"
                    className="text-red-500 hover:bg-red-50 hover:text-red-600"
                    onClick={handleLogout}
                >
                    <LogOut className="mr-2 h-4 w-4" />
                    Sign Out from All Devices
                </Button>
            </div>
        </div>
    );
}
