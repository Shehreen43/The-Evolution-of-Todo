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

    // Derived State (Filtered & Sorted Tasks)
    const filteredTasks = React.useMemo(() => {
        let result = [...tasks];

        // Filter
        if (status === 'completed') result = result.filter(t => t.completed);
        if (status === 'pending') result = result.filter(t => !t.completed);

        // Sort
        result.sort((a, b) => {
            const valA = a[sortBy] || '';
            const valB = b[sortBy] || '';
            if (valA < valB) return sortOrder === 'asc' ? -1 : 1;
            if (valA > valB) return sortOrder === 'asc' ? 1 : -1;
            return 0;
        });

        return result;
    }, [tasks, status, sortBy, sortOrder]);

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
        <div className="space-y-10">
            <DashboardHero user={{ name: session?.user?.name || '' }} />

            <TaskStats tasks={tasks} />

            <TaskFilters
                currentStatus={status}
                onStatusChange={setStatus}
                currentSort={sortBy}
                onSortChange={setSortBy}
                currentOrder={sortOrder}
                onOrderChange={setSortOrder}
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
