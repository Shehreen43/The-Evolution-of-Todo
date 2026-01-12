'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { Loader2 } from 'lucide-react';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'danger' | 'ghost' | 'outline';
    size?: 'sm' | 'md' | 'lg' | 'icon';
    isLoading?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
    ({ className, variant = 'primary', size = 'md', isLoading, disabled, children, ...props }, ref) => {
        const variants = {
            primary: 'bg-emerald-600 text-white hover:bg-emerald-700 active:bg-emerald-800 shadow-sm',
            secondary: 'bg-emerald-100 text-emerald-900 hover:bg-emerald-200 active:bg-emerald-300',
            danger: 'bg-red-600 text-white hover:bg-red-700 active:bg-red-800 shadow-sm',
            ghost: 'bg-transparent text-emerald-700 hover:bg-emerald-50 active:bg-emerald-100',
            outline: 'bg-transparent border border-emerald-600 text-emerald-700 hover:bg-emerald-50 active:bg-emerald-100',
        };

        const sizes = {
            sm: 'px-3 py-1.5 text-sm',
            md: 'px-4 py-2',
            lg: 'px-6 py-3 text-lg',
            icon: 'p-2 w-10 h-10 flex items-center justify-center',
        };

        return (
            <button
                ref={ref}
                className={cn(
                    'inline-flex items-center justify-center rounded-lg font-medium transition-all focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed',
                    variants[variant],
                    sizes[size],
                    className
                )}
                disabled={isLoading || disabled}
                {...props}
            >
                {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
                {!isLoading && children}
                {isLoading && size !== 'icon' && ' Loading...'}
            </button>
        );
    }
);
Button.displayName = 'Button';

export { Button };
