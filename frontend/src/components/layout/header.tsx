'use client';

import * as React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { CheckSquare, Menu, X } from 'lucide-react';
import { UserMenu } from '@/components/auth/user-menu';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui';

export function Header() {
    const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);
    const pathname = usePathname();

    const navLinks = [
        { name: 'Dashboard', href: '/dashboard' },
        { name: 'My Tasks', href: '/tasks' },
    ];

    return (
        <header className="sticky top-0 z-40 w-full border-b border-gray-100 bg-white/80 backdrop-blur-md">
            <div className="container mx-auto flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
                {/* Logo */}
                <Link href="/dashboard" className="flex items-center gap-2 group">
                    <div className="rounded-xl bg-emerald-600 p-1.5 transition-transform group-hover:scale-110 group-active:scale-95 shadow-sm">
                        <CheckSquare className="h-6 w-6 text-white" />
                    </div>
                    <span className="text-xl font-bold tracking-tight text-gray-900">
                        Hackathon<span className="text-emerald-600">Todo</span>
                    </span>
                </Link>

                {/* Desktop Navigation */}
                <nav className="hidden md:flex md:items-center md:gap-8">
                    {navLinks.map((link) => (
                        <Link
                            key={link.href}
                            href={link.href}
                            className={cn(
                                "text-sm font-semibold transition-colors hover:text-emerald-600",
                                pathname.startsWith(link.href) ? "text-emerald-600" : "text-gray-600"
                            )}
                        >
                            {link.name}
                        </Link>
                    ))}
                </nav>

                {/* User Menu & Mobile Toggle */}
                <div className="flex items-center gap-4">
                    <UserMenu />
                    <Button
                        variant="ghost"
                        size="icon"
                        className="md:hidden"
                        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                    >
                        {isMobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
                    </Button>
                </div>
            </div>

            {/* Mobile Menu */}
            {isMobileMenuOpen && (
                <div className="border-t bg-white p-4 md:hidden animate-in slide-in-from-top duration-200">
                    <nav className="flex flex-col gap-2">
                        {navLinks.map((link) => (
                            <Link
                                key={link.href}
                                href={link.href}
                                onClick={() => setIsMobileMenuOpen(false)}
                                className={cn(
                                    "rounded-lg px-4 py-3 text-sm font-bold transition-all active:scale-95",
                                    pathname.startsWith(link.href)
                                        ? "bg-emerald-50 text-emerald-700"
                                        : "text-gray-600 hover:bg-gray-50 uppercase tracking-wide"
                                )}
                            >
                                {link.name}
                            </Link>
                        ))}
                    </nav>
                </div>
            )}
        </header>
    );
}
