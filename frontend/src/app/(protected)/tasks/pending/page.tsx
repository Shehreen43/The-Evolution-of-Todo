'use client';

import React from 'react';
import { useSession } from '@/lib/auth-client';
import { useTasks } from '@/hooks/useTasks';
import { TaskList, TaskStats } from '@/components/tasks';
import { TaskFilters } from '@/components/tasks/task-filters';
import { TaskForm } from '@/components/tasks/task-form';
import { Modal, Button } from '@/components/ui';
import { Task, CreateTaskInput, UpdateTaskInput } from '@/types';
import { useReminderNotifications } from '@/hooks/useReminderNotifications';
import { Plus, Circle, Clock } from 'lucide-react';

export default function PendingTasksPage() {
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

  // Filter for pending tasks only
  const pendingTasks = allTasks.filter(task => !task.completed);

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
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-amber-500 to-orange-600 p-8 text-white">
        <div className="relative z-10">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold tracking-tight font-outfit flex items-center gap-3">
                <Circle className="h-10 w-10" />
                Pending Tasks
              </h1>
              <p className="text-amber-100 mt-2 text-lg">
                Focus on what needs to be done next
              </p>
            </div>
            <div className="hidden md:block">
              <Clock className="h-20 w-20 text-amber-200 opacity-80" />
            </div>
          </div>

          <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-4">
              <p className="text-amber-100 text-sm">Total Pending</p>
              <p className="text-3xl font-bold">{pendingTasks.length}</p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-4">
              <p className="text-amber-100 text-sm">Overdue</p>
              <p className="text-3xl font-bold">
                {pendingTasks.filter(t => t.due_date && new Date(t.due_date) < new Date() && !t.completed).length}
              </p>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-4">
              <p className="text-amber-100 text-sm">Due Soon</p>
              <p className="text-3xl font-bold">
                {pendingTasks.filter(t => t.due_date &&
                  new Date(t.due_date) >= new Date() &&
                  new Date(t.due_date) <= new Date(Date.now() + 86400000 * 3) &&
                  !t.completed
                ).length}
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

      <TaskStats tasks={pendingTasks} />

      <div className="bg-white rounded-3xl border border-gray-100 shadow-sm overflow-hidden">
        <div className="p-6 md:p-8 space-y-8">
          <TaskFilters
            currentStatus="pending"
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
            tasks={pendingTasks}
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

