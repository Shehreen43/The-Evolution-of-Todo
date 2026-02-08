'use client';

import React from 'react';
import { useSession } from '@/lib/auth-client';
import { useTasks } from '@/hooks/useTasks';
import { TaskList, TaskStats } from '@/components/tasks';
import { TaskFilters } from '@/components/tasks/task-filters';
import { TaskForm } from '@/components/tasks/task-form';
import { Modal } from '@/components/ui';
import { Task, CreateTaskInput, UpdateTaskInput } from '@/types';
import { useReminderNotifications } from '@/hooks/useReminderNotifications';
import { CheckCircle2, Trophy } from 'lucide-react';

export default function CompletedTasksPage() {
  const { data: session, isPending: isAuthLoading } = useSession();
  const [isModalOpen, setIsModalOpen] = React.useState(false);
  const [editingTask, setEditingTask] = React.useState<Task | undefined>(undefined);

  const {
    tasks: allTasks,
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
    createTask,
    updateTask,
    deleteTask,
    toggleComplete
  } = useTasks(session?.user?.id);

  // Initialize reminder notifications for all tasks
  useReminderNotifications(allTasks);

  // Filter for completed tasks only
  const completedTasks = allTasks.filter(task => task.completed);

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
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-emerald-500 to-teal-600 p-8 text-white">
        <div className="relative z-10">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold tracking-tight font-outfit flex items-center gap-3">
                <CheckCircle2 className="h-10 w-10" />
                Completed Tasks
              </h1>
              <p className="text-emerald-100 mt-2 text-lg">
                Celebrate your achievements and track your progress
              </p>
            </div>
            <div className="hidden md:block">
              <Trophy className="h-20 w-20 text-emerald-200 opacity-80" />
            </div>
          </div>

          <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-4">
              <p className="text-emerald-100 text-sm">Total Completed</p>
              <p className="text-3xl font-bold">{completedTasks.length}</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-4">
              <p className="text-emerald-100 text-sm">This Week</p>
              <p className="text-3xl font-bold">
                {completedTasks.filter(t => {
                  const weekAgo = new Date();
                  weekAgo.setDate(weekAgo.getDate() - 7);
                  return new Date(t.updated_at) > weekAgo;
                }).length}
              </p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-4">
              <p className="text-emerald-100 text-sm">This Month</p>
              <p className="text-3xl font-bold">
                {completedTasks.filter(t => {
                  const monthAgo = new Date();
                  monthAgo.setMonth(monthAgo.getMonth() - 1);
                  return new Date(t.updated_at) > monthAgo;
                }).length}
              </p>
            </div>
          </div>
        </div>

        {/* Background decorations */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-20 -right-20 h-80 w-80 rounded-full bg-white/10"></div>
          <div className="absolute -bottom-20 -left-20 h-80 w-80 rounded-full bg-white/5"></div>
        </div>
      </div>

      <TaskStats tasks={completedTasks} />

      <div className="bg-white rounded-3xl border border-gray-100 shadow-sm overflow-hidden">
        <div className="p-6 md:p-8 space-y-8">
          <TaskFilters
            currentStatus="completed"
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

          <TaskList
            tasks={completedTasks}
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