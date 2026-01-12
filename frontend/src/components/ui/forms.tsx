'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';

// --- Input ---
export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    error?: string;
    helperText?: string;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
    ({ className, type, label, error, helperText, ...props }, ref) => {
        return (
            <div className="w-full space-y-1.5">
                {label && (
                    <label className="text-sm font-medium text-gray-700 flex justify-between">
                        {label}
                        {props.required && <span className="text-emerald-600">*</span>}
                    </label>
                )}
                <input
                    type={type}
                    className={cn(
                        'flex h-10 w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm ring-offset-white file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-gray-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 transition-all shadow-sm',
                        error && 'border-red-500 focus-visible:ring-red-500',
                        className
                    )}
                    ref={ref}
                    {...props}
                />
                {error && <p className="text-xs font-medium text-red-500">{error}</p>}
                {helperText && !error && <p className="text-xs text-gray-500">{helperText}</p>}
            </div>
        );
    }
);
Input.displayName = 'Input';

// --- Textarea ---
export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
    label?: string;
    error?: string;
    helperText?: string;
}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
    ({ className, label, error, helperText, ...props }, ref) => {
        return (
            <div className="w-full space-y-1.5">
                {label && (
                    <label className="text-sm font-medium text-gray-700">
                        {label}
                    </label>
                )}
                <textarea
                    className={cn(
                        'flex min-h-[80px] w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm ring-offset-white placeholder:text-gray-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 transition-all shadow-sm',
                        error && 'border-red-500 focus-visible:ring-red-500',
                        className
                    )}
                    ref={ref}
                    {...props}
                />
                {error && <p className="text-xs font-medium text-red-500">{error}</p>}
                {helperText && !error && <p className="text-xs text-gray-500">{helperText}</p>}
            </div>
        );
    }
);
Textarea.displayName = 'Textarea';

// --- Checkbox ---
export interface CheckboxProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    error?: string;
}

const Checkbox = React.forwardRef<HTMLInputElement, CheckboxProps>(
    ({ className, label, error, ...props }, ref) => {
        return (
            <div className="space-y-1.5">
                <label className="flex items-center space-x-2 cursor-pointer group">
                    <div className="relative flex items-center">
                        <input
                            type="checkbox"
                            className={cn(
                                'peer h-5 w-5 cursor-pointer appearance-none rounded border border-gray-300 bg-white transition-all checked:border-emerald-600 checked:bg-emerald-600 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 disabled:opacity-50',
                                error && 'border-red-500',
                                className
                            )}
                            ref={ref}
                            {...props}
                        />
                        <svg
                            className="absolute left-1 top-1 h-3 w-3 pointer-events-none stroke-white opacity-0 transition-opacity peer-checked:opacity-100"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                            strokeWidth="4"
                        >
                            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                    </div>
                    {label && (
                        <span className="text-sm font-medium text-gray-700 group-hover:text-emerald-700 transition-colors">
                            {label}
                        </span>
                    )}
                </label>
                {error && <p className="text-xs font-medium text-red-500">{error}</p>}
            </div>
        );
    }
);
Checkbox.displayName = 'Checkbox';

export { Input, Textarea, Checkbox };
