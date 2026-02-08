'use client';

import * as React from 'react';
import { Task } from '@/types';
import { Pencil, Trash, Clock, CheckCircle2, Circle, Calendar, Bell, Repeat } from 'lucide-react';
import { formatDistanceToNow, format, isBefore } from 'date-fns';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui';

interface TaskCardProps {
    task: Task;
    onToggle: (id: number) => Promise<void>;
    onEdit: (task: Task) => void;
    onDelete: (id: number) => Promise<void>;
}

export function TaskCard({ task, onToggle, onEdit, onDelete }: TaskCardProps) {
    const [isToggling, setIsToggling] = React.useState(false);
    const [isDeleting, setIsDeleting] = React.useState(false);

    const handleToggle = async () => {
        setIsToggling(true);
        try {
            await onToggle(task.id);
        } finally {
            setIsToggling(false);
        }
    };

    const handleDelete = async () => {
        if (confirm('Are you sure you want to delete this task?')) {
            setIsDeleting(true);
            try {
                await onDelete(task.id);
            } finally {
                setIsDeleting(false);
            }
        }
    };

    const priorityColors = {
        low: 'bg-blue-100 text-blue-700',
        medium: 'bg-amber-100 text-amber-700',
        high: 'bg-red-100 text-red-700',
    };

    // Helper to check if task is overdue
    const isOverdue = task.due_date && !task.completed && isBefore(new Date(task.due_date), new Date());

    return (
        <div
            className={cn(
                'group relative flex flex-col justify-between rounded-2xl border bg-white p-5 transition-all hover:shadow-xl hover:-translate-y-1',
                task.completed ? 'border-emerald-100 bg-emerald-50/30' :
                isOverdue ? 'border-red-200 bg-red-50/30' : 'border-gray-200 shadow-sm'
            )}
        >
            <div className="flex items-start justify-between gap-4">
                <button
                    onClick={handleToggle}
                    disabled={isToggling}
                    className={cn(
                        'mt-1 flex-shrink-0 transition-transform active:scale-95',
                        isToggling && 'opacity-50 cursor-not-allowed'
                    )}
                >
                    {task.completed ? (
                        <CheckCircle2 className="h-6 w-6 text-emerald-600 fill-emerald-50" />
                    ) : (
                        <Circle className="h-6 w-6 text-gray-300 group-hover:text-emerald-500" />
                    )}
                </button>

                <div className="flex-1 min-w-0">
                    <h3
                        className={cn(
                            'text-lg font-semibold transition-all truncate',
                            task.completed ? 'text-gray-400 line-through' :
                            isOverdue ? 'text-red-600' : 'text-gray-800'
                        )}
                    >
                        {task.title}
                    </h3>
                    {task.description && (
                        <p className={cn(
                            'mt-1 text-sm line-clamp-2',
                            task.completed ? 'text-gray-400' :
                            isOverdue ? 'text-red-600' : 'text-gray-600'
                        )}>
                            {task.description}
                        </p>
                    )}

                    {/* Advanced task information */}
                    <div className="mt-3 flex flex-wrap gap-2">
                        {task.due_date && (
                            <div className={cn(
                                'flex items-center gap-1 text-xs px-2 py-1 rounded-full',
                                isOverdue ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'
                            )}>
                                <Calendar className="h-3 w-3" />
                                {format(new Date(task.due_date), 'MMM dd, HH:mm')}
                            </div>
                        )}

                        {task.reminder_time && (
                            <div className="flex items-center gap-1 text-xs px-2 py-1 rounded-full bg-purple-100 text-purple-700">
                                <Bell className="h-3 w-3" />
                                {format(new Date(task.reminder_time), 'MMM dd, HH:mm')}
                            </div>
                        )}

                        {task.category && (
                            <div className="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-700">
                                #{task.category}
                            </div>
                        )}

                        {task.is_recurring && (
                            <div className="flex items-center gap-1 text-xs px-2 py-1 rounded-full bg-green-100 text-green-700">
                                <Repeat className="h-3 w-3" />
                                {task.recurrence_pattern || 'Recurring'}
                            </div>
                        )}
                    </div>
                </div>
            </div>

            <div className="mt-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    {task.priority && (
                        <span className={cn('rounded-full px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider', priorityColors[task.priority])}>
                            {task.priority}
                        </span>
                    )}
                    <div className="flex items-center text-[11px] text-gray-400">
                        <Clock className="mr-1 h-3 w-3" />
                        {formatDistanceToNow(new Date(task.created_at), { addSuffix: true })}
                    </div>
                </div>

                <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => onEdit(task)}
                        className="h-8 w-8 text-gray-400 hover:text-emerald-600"
                    >
                        <Pencil className="h-4 w-4" />
                    </Button>
                    <Button
                        variant="ghost"
                        size="icon"
                        onClick={handleDelete}
                        isLoading={isDeleting}
                        className="h-8 w-8 text-gray-400 hover:text-red-600"
                    >
                        <Trash className="h-4 w-4" />
                    </Button>
                </div>
            </div>
        </div>
    );
}
