'use client';

import * as React from 'react';
import { useSession, signOut } from '@/lib/auth-client';
import { useRouter } from 'next/navigation';
import {
    LogOut,
    User as UserIcon,
    LayoutDashboard,
    Settings,
    ChevronDown
} from 'lucide-react';
import { showToast } from '@/components/ui';
import { cn } from '@/lib/utils';
import Link from 'next/link';

export function UserMenu() {
    const { data: session } = useSession();
    const router = useRouter();
    const [isOpen, setIsOpen] = React.useState(false);
    const menuRef = React.useRef<HTMLDivElement>(null);

    // Close on click outside
    React.useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    if (!session?.user) return null;

    const handleSignOut = async () => {
        try {
            await signOut();

            showToast.success('Logged out successfully');
            router.push('/');
        } catch {
            // Even if something fails, we should try to clear local state and redirect
            showToast.error('Logout completed with warnings');
            router.push('/');
        }
    };

    const initials = session.user.name
        ? session.user.name.split(' ').map(n => n[0]).join('').toUpperCase()
        : 'U';

    return (
        <div className="relative" ref={menuRef}>
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center gap-3 rounded-full border border-gray-100 bg-white p-1.5 pr-4 transition-all hover:bg-gray-50 hover:shadow-sm"
            >
                <div className="flex h-9 w-9 items-center justify-center rounded-full bg-emerald-600 text-sm font-bold text-white shadow-inner">
                    {initials}
                </div>
                <div className="hidden text-left md:block">
                    <p className="max-w-[120px] truncate text-sm font-bold text-gray-900">
                        {session.user.name}
                    </p>
                    <p className="text-[11px] text-gray-500">{session.user.email}</p>
                </div>
                <ChevronDown className={cn("h-4 w-4 text-gray-400 transition-transform", isOpen && "rotate-180")} />
            </button>

            {isOpen && (
                <div className="absolute right-0 mt-2 w-56 origin-top-right rounded-2xl border border-gray-100 bg-white p-2 shadow-2xl animate-in fade-in zoom-in-95 duration-100 z-50">
                    <div className="px-3 py-2 md:hidden">
                        <p className="text-sm font-bold text-gray-900">{session.user.name}</p>
                        <p className="text-xs text-gray-500">{session.user.email}</p>
                        <div className="my-2 border-t" />
                    </div>

                    <Link
                        href="/dashboard"
                        onClick={() => setIsOpen(false)}
                        className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-gray-700 hover:bg-emerald-50 hover:text-emerald-700 transition-all"
                    >
                        <LayoutDashboard className="h-4 w-4" />
                        Dashboard
                    </Link>

                    <Link
                        href="/profile"
                        onClick={() => setIsOpen(false)}
                        className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-gray-700 hover:bg-emerald-50 hover:text-emerald-700 transition-all"
                    >
                        <UserIcon className="h-4 w-4" />
                        My Profile
                    </Link>

                    <Link
                        href="/settings"
                        onClick={() => setIsOpen(false)}
                        className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium text-gray-700 hover:bg-emerald-50 hover:text-emerald-700 transition-all"
                    >
                        <Settings className="h-4 w-4" />
                        Settings
                    </Link>

                    <div className="my-1 border-t border-gray-100" />

                    <button
                        onClick={handleSignOut}
                        className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-bold text-red-600 hover:bg-red-50 transition-all"
                    >
                        <LogOut className="h-4 w-4" />
                        Sign Out
                    </button>
                </div>
            )}
        </div>
    );
}
