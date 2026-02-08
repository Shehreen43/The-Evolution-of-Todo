'use client';

import * as React from 'react';
import { useSession } from '@/lib/auth-client';
import { api } from '@/lib/api';
import { CreateTaskInput, Task, UpdateTaskInput, TaskStatus, SortField, SortOrder } from '@/types';
import { DashboardHero } from '@/components/layout/page-layouts';
import { TaskList, TaskStats } from '@/components/tasks';
import { TaskFilters } from '@/components/tasks/task-filters';
import { Button, showToast, Modal } from '@/components/ui';
import { TaskForm } from '@/components/tasks/task-form';
import { useReminderNotifications } from '@/hooks/useReminderNotifications';
import { Plus } from 'lucide-react';

export default function DashboardPage() {
    const { data: session, isPending: isAuthLoading } = useSession();
    const [tasks, setTasks] = React.useState<Task[]>([]);
    const [isLoading, setIsLoading] = React.useState(true);
    const [isModalOpen, setIsModalOpen] = React.useState(false);
    const [editingTask, setEditingTask] = React.useState<Task | undefined>(undefined);

    // Filter & Sort State
    const [status, setStatus] = React.useState<TaskStatus>('all');
    const [sortBy, setSortBy] = React.useState<SortField>('created_at');
    const [sortOrder, setSortOrder] = React.useState<SortOrder>('desc');
    const [category, setCategory] = React.useState<string>('');
    const [dueDateFilter, setDueDateFilter] = React.useState<string>('');
    const [recurringFilter, setRecurringFilter] = React.useState<boolean | 'all'>('all');

    // Fetch Tasks
    const fetchTasks = React.useCallback(async () => {
        if (!session?.user?.id) return;
        setIsLoading(true);
        try {
            const data = await api.getTasks(session.user.id);
            setTasks(data);
        } catch {
            showToast.error('Failed to load tasks');
        } finally {
            setIsLoading(false);
        }
    }, [session?.user?.id]);

    React.useEffect(() => {
        if (session?.user) {
            fetchTasks();
        }
    }, [session, fetchTasks]);

    // Initialize reminder notifications
    useReminderNotifications(tasks);

    // Derived State (Filtered & Sorted Tasks)
    const filteredTasks = React.useMemo(() => {
        let result = [...tasks];

        // Filter by status
        if (status === 'completed') result = result.filter(t => t.completed);
        if (status === 'pending') result = result.filter(t => !t.completed);

        // Filter by category
        if (category === 'category') {
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
                    if (sortBy === 'due_date' as SortField && valA && valB) {
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

    // Handle Create/Update
    const handleSubmit = async (data: CreateTaskInput | UpdateTaskInput) => {
        if (!session?.user?.id) return;
        try {
            if (editingTask) {
                const updatedTask = await api.updateTask(session.user.id, editingTask.id, data);
                setTasks(prev => prev.map(t => t.id === updatedTask.id ? updatedTask : t));
                showToast.success('Task updated');
            } else {
                const newTask = await api.createTask(session.user.id, data as CreateTaskInput);
                setTasks(prev => [newTask, ...prev]);
                showToast.success('Task created');
            }
            setIsModalOpen(false);
            setEditingTask(undefined);
        } catch {
            showToast.error('Operation failed');
        }
    };

    // Handle Toggle (Optimistic)
    const handleToggle = async (taskId: number) => {
        if (!session?.user?.id) return;

        // Optimistic Update
        const previousTasks = [...tasks];
        setTasks(prev => prev.map(t => t.id === taskId ? { ...t, completed: !t.completed } : t));

        try {
            await api.toggleComplete(session.user.id, taskId);
        } catch {
            setTasks(previousTasks);
            showToast.error('Failed to update status');
        }
    };

    // Handle Delete (Optimistic)
    const handleDelete = async (taskId: number) => {
        if (!session?.user?.id) return;

        const previousTasks = [...tasks];
        setTasks(prev => prev.filter(t => t.id !== taskId));

        try {
            await api.deleteTask(session.user.id, taskId);
            showToast.success('Task deleted');
        } catch {
            setTasks(previousTasks);
            showToast.error('Failed to delete task');
        }
    };

    const handleEdit = (task: Task) => {
        setEditingTask(task);
        setIsModalOpen(true);
    };

    return (
        <div className="space-y-5">
            <DashboardHero user={{ name: session?.user?.name || '' }} />

            <TaskStats tasks={tasks} />

            <TaskFilters
                currentStatus={status}
                onStatusChange={setStatus}
                currentSort={sortBy}
                onSortChange={setSortBy}
                currentOrder={sortOrder}
                onOrderChange={setSortOrder}
                currentCategory={category}
                onCategoryChange={setCategory}
                currentDueDateFilter={dueDateFilter}
                onDueDateFilterChange={setDueDateFilter}
                currentRecurringFilter={recurringFilter}
                onRecurringFilterChange={setRecurringFilter}
            />

            <div className="flex items-center justify-between">
                <h3 className="text-2xl font-bold text-gray-900">Recent Tasks</h3>
                <Button
                    onClick={() => { setEditingTask(undefined); setIsModalOpen(true); }}
                    className="rounded-full px-6 shadow-md shadow-emerald-100"
                >
                    <Plus className="mr-2 h-5 w-5" />
                    New Task
                </Button>
            </div>

            <TaskList
                tasks={filteredTasks}
                loading={isLoading || isAuthLoading}
                onToggle={handleToggle}
                onEdit={handleEdit}
                onDelete={handleDelete}
            />

            {/* Task Creation/Edit Modal */}
            <Modal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                title={editingTask ? 'Edit Task' : 'Create New Task'}
            >
                <TaskForm
                    initialData={editingTask}
                    onCancel={() => setIsModalOpen(false)}
                    onSubmit={handleSubmit}
                />
            </Modal>
        </div>
    );
}
