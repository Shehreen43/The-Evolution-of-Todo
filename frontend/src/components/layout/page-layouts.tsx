'use client';

import * as React from 'react';
import { Header } from './header';
import { Sidebar } from './sidebar';
import { cn } from '@/lib/utils';

// --- BaseShell (The Header + Sidebar structure) ---
interface BaseShellProps {
    children: React.ReactNode;
    showSidebar?: boolean;
}

export function BaseShell({ children, showSidebar = true }: BaseShellProps) {
    return (
        <div className="min-h-screen bg-[#fafafa]">
            <Header />
            <div className="container mx-auto flex px-4 sm:px-6 lg:px-8">
                {showSidebar && <Sidebar />}
                <main className={cn(
                    "flex-1 py-8 lg:py-12",
                    showSidebar && "lg:pl-10"
                )}>
                    {children}
                </main>
            </div>
        </div>
    );
}

// --- PageHeader (Title and Actions) ---
interface PageHeaderProps {
    title: string;
    description?: string;
    action?: React.ReactNode;
}

export function PageHeader({ title, description, action }: PageHeaderProps) {
    return (
        <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
                <h1 className="text-3xl font-extrabold tracking-tight text-gray-900">{title}</h1>
                {description && <p className="mt-1 text-gray-500">{description}</p>}
            </div>
            {action && <div className="flex-shrink-0">{action}</div>}
        </div>
    );
}

// --- DashboardHero (Special greeting for Dashboard) ---


export function DashboardHero({ user }: { user?: { name: string } }) {
    const currentHour = new Date().getHours();
    const greeting = currentHour < 12 ? 'Good morning' : currentHour < 18 ? 'Good afternoon' : 'Good evening';

    return (
        <section className="relative overflow-hidden rounded-[2.5rem] bg-emerald-700 p-8 text-white sm:p-12 shadow-2xl shadow-emerald-200 mb-10">
            <div className="relative z-10 max-w-2xl">
                <h2 className="text-3xl font-bold sm:text-4xl drop-shadow-lg">
                    {greeting}, <span className="text-emerald-300">{user?.name || 'Friend'}</span>!
                </h2>
                <p className="mt-4 text-emerald-100/80 sm:text-lg leading-relaxed drop-shadow">
                    You have some exciting things to tackle today. Every small task completed is a step towards greatness.
                </p>
            </div>
            <div className="absolute -right-20 -top-20 h-64 w-64 rounded-full bg-emerald-600/30 blur-3xl" />
            <div className="absolute -bottom-10 right-20 h-40 w-40 rounded-full bg-emerald-500/20 blur-2xl" />
        </section>
    );
}
