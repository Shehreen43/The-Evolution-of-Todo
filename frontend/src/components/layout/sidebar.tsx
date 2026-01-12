'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
    Home,
    ListTodo,
    CheckCircle2,
    Clock,
    PlusCircle,
    User,
    Zap
} from 'lucide-react';
import { cn } from '@/lib/utils';

export function Sidebar() {
    const pathname = usePathname();

    const menuItems = [
        { name: 'Dashboard', href: '/dashboard', icon: Home },
        { name: 'All Tasks', href: '/tasks', icon: ListTodo },
        { name: 'Completed', href: '/tasks/completed', icon: CheckCircle2 },
        { name: 'Pending', href: '/tasks/pending', icon: Clock },
        { name: 'New Task', href: '/tasks/new', icon: PlusCircle },
        { name: 'Profile', href: '/profile', icon: User },
    ];

    return (
        <aside className="hidden lg:flex w-64 flex-col border-r border-gray-100 bg-white p-6 min-h-[calc(100vh-64px)] overflow-y-auto">
            <div className="space-y-6">
                <div>
                    <h5 className="mb-4 px-4 text-[10px] font-bold uppercase tracking-widest text-gray-400">
                        Navigation
                    </h5>
                    <nav className="space-y-1">
                        {menuItems.map((item) => (
                            <Link
                                key={item.href}
                                href={item.href}
                                className={cn(
                                    'flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-semibold transition-all group',
                                    pathname === item.href
                                        ? 'bg-emerald-600 text-white shadow-md shadow-emerald-200'
                                        : 'text-gray-600 hover:bg-emerald-50 hover:text-emerald-700'
                                )}
                            >
                                <item.icon className={cn(
                                    "h-5 w-5 transition-transform group-hover:scale-110",
                                    pathname === item.href ? "text-white" : "text-gray-400 group-hover:text-emerald-600"
                                )} />
                                {item.name}
                            </Link>
                        ))}
                    </nav>
                </div>

                <div className="mt-8 rounded-3xl bg-emerald-50 p-6">
                    <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-2xl bg-emerald-600 text-white shadow-sm">
                        <Zap className="h-5 w-5" />
                    </div>
                    <h6 className="text-sm font-bold text-gray-900 leading-tight">Pro Accountability</h6>
                    <p className="mt-1 text-[11px] text-gray-500 leading-relaxed">
                        Upgrade to Phase III for AI-powered task prioritization.
                    </p>
                    <button className="mt-4 w-full rounded-xl bg-white py-2 text-xs font-bold text-emerald-700 shadow-sm transition-all hover:bg-emerald-100 active:scale-95">
                        Learn More
                    </button>
                </div>
            </div>
        </aside>
    );
}
