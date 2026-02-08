'use client';

import * as React from 'react';
import { api } from '@/lib/api';
import { Task, CreateTaskInput, UpdateTaskInput, TaskStatus, SortField, SortOrder } from '@/types';
import { showToast } from '@/components/ui';

export function useTasks(userId: string | undefined) {
    const [tasks, setTasks] = React.useState<Task[]>([]);
    const [isLoading, setIsLoading] = React.useState(true);
    const [status, setStatus] = React.useState<TaskStatus>('all');
    const [sortBy, setSortBy] = React.useState<SortField>('created_at');
    const [sortOrder, setSortOrder] = React.useState<SortOrder>('desc');
    const [category, setCategory] = React.useState<string>('');
    const [dueDateFilter, setDueDateFilter] = React.useState<string>('');
    const [recurringFilter, setRecurringFilter] = React.useState<boolean | 'all'>('all');

    const fetchTasks = React.useCallback(async () => {
        if (!userId) return;
        setIsLoading(true);
        try {
            const data = await api.getTasks(userId);
            setTasks(data);
        } catch {
            showToast.error('Failed to load tasks');
        } finally {
            setIsLoading(false);
        }
    }, [userId]);

    React.useEffect(() => {
        if (userId) {
            fetchTasks();
        }
    }, [userId, fetchTasks]);

    const filteredTasks = React.useMemo(() => {
        let result = [...tasks];

        // Filter by status
        if (status === 'completed') result = result.filter(t => t.completed);
        if (status === 'pending') result = result.filter(t => !t.completed);

        // Filter by category
        if (category) {
            result = result.filter(t => t.category?.toLowerCase() === category.toLowerCase());
        }

        // Filter by recurring status
        if (recurringFilter !== 'all') {
            result = result.filter(t => t.is_recurring === recurringFilter);
        }

        // Filter by due date
        if (dueDateFilter) {
            const now = new Date();
            const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
            const endOfWeek = new Date(today);
            endOfWeek.setDate(today.getDate() + 7);
            const endOfMonth = new Date(today);
            endOfMonth.setMonth(endOfMonth.getMonth() + 1);

            switch (dueDateFilter) {
                case 'today':
                    result = result.filter(t => {
                        if (!t.due_date) return false;
                        const dueDate = new Date(t.due_date);
                        return dueDate.toDateString() === today.toDateString();
                    });
                    break;
                case 'overdue':
                    result = result.filter(t => {
                        if (!t.due_date || t.completed) return false;
                        const dueDate = new Date(t.due_date);
                        return dueDate < now;
                    });
                    break;
                case 'week':
                    result = result.filter(t => {
                        if (!t.due_date) return false;
                        const dueDate = new Date(t.due_date);
                        return dueDate >= today && dueDate <= endOfWeek;
                    });
                    break;
                case 'month':
                    result = result.filter(t => {
                        if (!t.due_date) return false;
                        const dueDate = new Date(t.due_date);
                        return dueDate >= today && dueDate <= endOfMonth;
                    });
                    break;
            }
        }

        // Sort
        result.sort((a, b) => {
            let valA: any = a[sortBy];
            let valB: any = b[sortBy];

            // Handle date comparisons
            if (sortBy === 'due_date' && valA && valB) {
                valA = new Date(valA);
                valB = new Date(valB);
            } else if (sortBy === 'created_at' || sortBy === 'updated_at') {
                valA = new Date(valA);
                valB = new Date(valB);
            }

            if (valA < valB) return sortOrder === 'asc' ? -1 : 1;
            if (valA > valB) return sortOrder === 'asc' ? 1 : -1;
            return 0;
        });

        return result;
    }, [tasks, status, category, dueDateFilter, recurringFilter, sortBy, sortOrder]);

    const createTask = async (data: CreateTaskInput) => {
        if (!userId) return;
        try {
            const newTask = await api.createTask(userId, data);
            setTasks(prev => [newTask, ...prev]);
            showToast.success('Task created');
            return newTask;
        } catch {
            showToast.error('Failed to create task');
        }
    };

    const updateTask = async (taskId: number, data: UpdateTaskInput) => {
        if (!userId) return;
        try {
            const updatedTask = await api.updateTask(userId, taskId, data);
            setTasks(prev => prev.map(t => t.id === updatedTask.id ? updatedTask : t));
            showToast.success('Task updated');
            return updatedTask;
        } catch {
            showToast.error('Failed to update task');
        }
    };

    const deleteTask = async (taskId: number) => {
        if (!userId) return;
        const previousTasks = [...tasks];
        setTasks(prev => prev.filter(t => t.id !== taskId));
        try {
            await api.deleteTask(userId, taskId);
            showToast.success('Task deleted');
        } catch {
            setTasks(previousTasks);
            showToast.error('Failed to delete task');
        }
    };

    const toggleComplete = async (taskId: number) => {
        if (!userId) return;
        const previousTasks = [...tasks];
        setTasks(prev => prev.map(t => t.id === taskId ? { ...t, completed: !t.completed } : t));
        try {
            await api.toggleComplete(userId, taskId);
        } catch {
            setTasks(previousTasks);
            showToast.error('Failed to update status');
        }
    };

    return {
        tasks: filteredTasks,
        isLoading,
        status,
        setStatus,
        sortBy,
        setSortBy,
        sortOrder,
        setSortOrder,
        category,
        setCategory,
        dueDateFilter,
        setDueDateFilter,
        recurringFilter,
        setRecurringFilter,
        fetchTasks,
        createTask,
        updateTask,
        deleteTask,
        toggleComplete
    };
}
