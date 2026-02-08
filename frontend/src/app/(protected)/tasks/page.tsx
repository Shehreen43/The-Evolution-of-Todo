'use client';

import React from 'react';
import { useSession } from '@/lib/auth-client';
import { useTasks } from '@/hooks/useTasks';
import { useReminderNotifications } from '@/hooks/useReminderNotifications';
import { TaskList, TaskStats } from '@/components/tasks';
import { TaskFilters } from '@/components/tasks/task-filters';
import { TaskForm } from '@/components/tasks/task-form';
import { Modal, Button } from '@/components/ui';
import { Task, CreateTaskInput, UpdateTaskInput } from '@/types';
import { Plus } from 'lucide-react';

export default function TasksPage() {
  const { data: session, isPending: isAuthLoading } = useSession();
  const [isModalOpen, setIsModalOpen] = React.useState(false);
  const [editingTask, setEditingTask] = React.useState<Task | undefined>(undefined);

  const {
    tasks: filteredTasks,
    isLoading,
    status,
    setStatus,
    sortBy,
    setSortBy,
    sortOrder,
    setSortOrder,
    createTask,
    updateTask,
    deleteTask,
    toggleComplete
  } = useTasks(session?.user?.id);

  // Initialize reminder notifications
  useReminderNotifications(filteredTasks);

  const handleSubmit = async (data: CreateTaskInput | UpdateTaskInput) => {
    if (editingTask) {
      await updateTask(editingTask.id, data as UpdateTaskInput);
    } else {
      await createTask(data as CreateTaskInput);
    }
    setIsModalOpen(false);
    setEditingTask(undefined);
  };

  const handleEdit = (task: Task) => {
    setEditingTask(task);
    setIsModalOpen(true);
  };

  const handleCancel = () => {
    setIsModalOpen(false);
    setEditingTask(undefined);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-gray-900 font-outfit">My Tasks</h1>
          <p className="text-gray-500 mt-1">
            Manage your daily goals and track your progress.
          </p>
        </div>
        <Button
          onClick={() => { setEditingTask(undefined); setIsModalOpen(true); }}
          className="rounded-full px-6 shadow-lg shadow-emerald-100 bg-emerald-600 hover:bg-emerald-700 text-white transition-all duration-300 transform hover:scale-105"
        >
          <Plus className="mr-2 h-5 w-5" />
          New Task
        </Button>
      </div>

      <TaskStats tasks={filteredTasks} />

      <div className="bg-white rounded-3xl border border-gray-100 shadow-sm overflow-hidden">
        <div className="p-6 md:p-8 space-y-8">
          <TaskFilters
            currentStatus={status}
            onStatusChange={setStatus}
            currentSort={sortBy}
            onSortChange={setSortBy}
            currentOrder={sortOrder}
            onOrderChange={setSortOrder}
          />

          <TaskList
            tasks={filteredTasks}
            loading={isLoading || isAuthLoading}
            onToggle={toggleComplete}
            onEdit={handleEdit}
            onDelete={deleteTask}
          />
        </div>
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={handleCancel}
        title={editingTask ? 'Edit Task' : 'Create New Task'}
      >
        <TaskForm
          initialData={editingTask}
          onCancel={handleCancel}
          onSubmit={handleSubmit}
        />
      </Modal>
    </div>
  );
}
