'use client';

import React from 'react';
import { TaskList, TaskStats } from '@/components/tasks';
import { TaskFilters } from '@/components/tasks/task-filters';
import { TaskForm } from '@/components/tasks/task-form';
import { TaskStatus, SortField, SortOrder } from '@/types';
import { TaskCard } from '@/components/tasks/task-card';

export default function TasksPage() {
  // State for filters
  const [status, setStatus] = React.useState<TaskStatus>('all');
  const [sortBy, setSortBy] = React.useState<SortField>('created_at');
  const [sortOrder, setSortOrder] = React.useState<SortOrder>('desc');

  // Empty handlers for now (will be implemented with full functionality later)
  const handleToggle = async (id: number) => {
    console.log('Toggle task:', id);
  };

  const handleEdit = (task: any) => {
    console.log('Edit task:', task);
  };

  const handleDelete = async (id: number) => {
    console.log('Delete task:', id);
  };

  const handleSubmit = async (data: any) => {
    console.log('Create task:', data);
  };

  const handleCancel = () => {
    console.log('Cancel task creation');
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">My Tasks</h1>
        <p className="text-muted-foreground">
          Manage your tasks and track your progress.
        </p>
      </div>

      <TaskStats tasks={[]} />

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <div className="border rounded-lg p-6 bg-white shadow-sm">
            <TaskFilters
              currentStatus={status}
              onStatusChange={setStatus}
              currentSort={sortBy}
              onSortChange={setSortBy}
              currentOrder={sortOrder}
              onOrderChange={setSortOrder}
            />
            <TaskList
              tasks={[]}
              loading={true}
              onToggle={handleToggle}
              onEdit={handleEdit}
              onDelete={handleDelete}
            />
          </div>
        </div>
        <div>
          <div className="border rounded-lg p-6 bg-white shadow-sm">
            <TaskForm onSubmit={handleSubmit} onCancel={handleCancel} />
          </div>
        </div>
      </div>
    </div>
  );
}