'use client';

import * as React from 'react';
import { Task } from '@/types';
import { CheckCircle2, ListTodo } from 'lucide-react';

interface TaskStatsProps {
    tasks?: Task[];
}

export function TaskStats({ tasks = [] }: TaskStatsProps) {
    const total = tasks.length;
    const completed = tasks.filter(t => t.completed).length;
    const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;

    return (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div className="flex items-center gap-4 rounded-3xl border border-emerald-100 bg-white p-6 shadow-sm">
                <div className="rounded-2xl bg-emerald-100 p-3">
                    <ListTodo className="h-6 w-6 text-emerald-600" />
                </div>
                <div>
                    <p className="text-sm font-medium text-gray-500">Total Tasks</p>
                    <h4 className="text-2xl font-bold text-gray-900">{total}</h4>
                </div>
            </div>

            <div className="flex items-center gap-4 rounded-3xl border border-emerald-100 bg-white p-6 shadow-sm">
                <div className="rounded-2xl bg-emerald-50 p-3">
                    <CheckCircle2 className="h-6 w-6 text-emerald-600" />
                </div>
                <div>
                    <p className="text-sm font-medium text-gray-500">Completed</p>
                    <h4 className="text-2xl font-bold text-gray-900">{completed}</h4>
                </div>
            </div>

            <div className="relative overflow-hidden rounded-3xl border border-emerald-100 bg-emerald-600 p-6 text-white shadow-lg">
                <div className="relative z-10">
                    <p className="text-sm font-medium text-emerald-100">Completion</p>
                    <h4 className="text-2xl font-bold">{percentage}%</h4>
                    <div className="mt-3 h-2 w-full rounded-full bg-emerald-500/50">
                        <div
                            className="h-full rounded-full bg-white transition-all duration-1000 ease-out"
                            style={{ width: `${percentage}%` }}
                        />
                    </div>
                </div>
                {/* Background decorations */}
                <div className="absolute -bottom-6 -right-6 h-24 w-24 rounded-full bg-emerald-500/20" />
                <div className="absolute -top-6 -left-6 h-16 w-16 rounded-full bg-emerald-700/20" />
            </div>
        </div>
    );
}
