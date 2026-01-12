'use client';

import { toast, Toaster } from 'react-hot-toast';

export const showToast = {
    success: (message: string) =>
        toast.success(message, {
            style: {
                borderRadius: '12px',
                background: '#059669', // Emerald 600
                color: '#fff',
                fontWeight: '500',
            },
            iconTheme: {
                primary: '#fff',
                secondary: '#059669',
            },
        }),
    error: (message: string) =>
        toast.error(message, {
            style: {
                borderRadius: '12px',
                background: '#dc2626', // Red 600
                color: '#fff',
                fontWeight: '500',
            },
            iconTheme: {
                primary: '#fff',
                secondary: '#dc2626',
            },
        }),
};

export { Toaster };
