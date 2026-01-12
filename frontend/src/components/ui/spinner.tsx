'use client';

import { cn } from '@/lib/utils';
import { Loader2 } from 'lucide-react';

interface SpinnerProps {
    className?: string;
    size?: 'sm' | 'md' | 'lg' | 'xl';
    variant?: 'emerald' | 'white' | 'gray';
}

export function Spinner({ className, size = 'md', variant = 'emerald' }: SpinnerProps) {
    const sizes = {
        sm: 'h-4 w-4',
        md: 'h-8 w-8',
        lg: 'h-12 w-12',
        xl: 'h-16 w-16',
    };

    const variants = {
        emerald: 'text-emerald-600',
        white: 'text-white',
        gray: 'text-gray-400',
    };

    return (
        <Loader2
            className={cn('animate-spin', sizes[size], variants[variant], className)}
        />
    );
}
