'use client';

import * as React from 'react';
import { useForm, useWatch } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Task } from '@/types';
import { Input, Textarea, Button } from '@/components/ui';
import { cn } from '@/lib/utils';

const taskSchema = z.object({
    title: z.string().min(1, 'Title is required').max(200, 'Title too long'),
    description: z.string().max(1000, 'Description too long').optional(),
    priority: z.enum(['low', 'medium', 'high']),
});

type TaskFormData = z.infer<typeof taskSchema>;

interface TaskFormProps {
    initialData?: Task;
    onSubmit: (data: TaskFormData) => Promise<void>;
    onCancel: () => void;
    isLoading?: boolean;
}

export function TaskForm({ initialData, onSubmit, onCancel, isLoading }: TaskFormProps) {
    const {
        register,
        handleSubmit,
        formState: { errors },
        control,
    } = useForm<TaskFormData>({
        resolver: zodResolver(taskSchema),
        defaultValues: {
            title: initialData?.title || '',
            description: initialData?.description || '',
            priority: initialData?.priority || 'medium',
        },
    });

    const titleValue = useWatch({ control, name: 'title' }) || '';
    const descriptionValue = useWatch({ control, name: 'description' }) || '';

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <Input
                label="Task Title"
                placeholder="What needs to be done?"
                error={errors.title?.message}
                required
                {...register('title')}
                helperText={`${titleValue.length}/200`}
            />

            <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">Priority</label>
                <div className="flex gap-4">
                    {['low', 'medium', 'high'].map((p) => (
                        <label key={p} className="flex items-center cursor-pointer">
                            <input
                                type="radio"
                                value={p}
                                className="peer hidden"
                                {...register('priority')}
                            />
                            <div className={cn(
                                "px-4 py-2 rounded-full border text-sm font-medium transition-all",
                                "peer-checked:bg-emerald-600 peer-checked:text-white peer-checked:border-emerald-600",
                                "hover:bg-emerald-50 text-gray-600"
                            )}>
                                {p.charAt(0).toUpperCase() + p.slice(1)}
                            </div>
                        </label>
                    ))}
                </div>
            </div>

            <Textarea
                label="Description (Optional)"
                placeholder="Add more details..."
                error={errors.description?.message}
                rows={4}
                {...register('description')}
                helperText={`${descriptionValue.length}/1000`}
            />

            <div className="flex justify-end gap-3 pt-4">
                <Button variant="ghost" type="button" onClick={onCancel}>
                    Cancel
                </Button>
                <Button type="submit" isLoading={isLoading}>
                    {initialData ? 'Update Task' : 'Create Task'}
                </Button>
            </div>
        </form>
    );
}

