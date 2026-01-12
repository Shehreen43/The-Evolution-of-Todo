'use client';

import * as React from 'react';
import { Task } from '@/types';
import { TaskCard } from './task-card';
import { Spinner } from '@/components/ui';
import { ClipboardList } from 'lucide-react';

interface TaskListProps {
    tasks: Task[];
    loading: boolean;
    onToggle: (id: number) => Promise<void>;
    onEdit: (task: Task) => void;
    onDelete: (id: number) => Promise<void>;
}

export function TaskList({ tasks, loading, onToggle, onEdit, onDelete }: TaskListProps) {
    if (loading && tasks.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center py-20">
                <Spinner size="lg" />
                <p className="mt-4 text-gray-500 font-medium">Loading your tasks...</p>
            </div>
        );
    }

    if (tasks.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center py-20 rounded-3xl border-2 border-dashed border-gray-100 bg-gray-50/50">
                <div className="rounded-full bg-emerald-100 p-6">
                    <ClipboardList className="h-12 w-12 text-emerald-600" />
                </div>
                <h3 className="mt-6 text-xl font-bold text-gray-900">No tasks found</h3>
                <p className="mt-2 text-gray-500 max-w-xs text-center">
                    It look like you haven&apos;t created any tasks yet. Time to get productive!
                </p>
            </div>
        );
    }

    return (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {tasks.map((task) => (
                <TaskCard
                    key={task.id}
                    task={task}
                    onToggle={onToggle}
                    onEdit={onEdit}
                    onDelete={onDelete}
                />
            ))}
        </div>
    );
}
