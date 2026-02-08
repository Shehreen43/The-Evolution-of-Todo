import React, { useState } from 'react';
import { Task } from '@/lib/api';
import { ConfirmDialog } from '../ui/ConfirmDialog';

interface TaskItemProps {
  task: Task;
  onToggle: (taskId: number) => void;
  onDelete: (taskId: number) => void;
  onEdit: (taskId: number, updates: Partial<Task>) => void;
}

export function TaskItem({ task, onToggle, onDelete, onEdit }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [isDeleteConfirmOpen, setIsDeleteConfirmOpen] = useState(false);

  const handleDeleteConfirm = () => {
    onDelete(task.id);
    setIsDeleteConfirmOpen(false);
  };

  return (
    <>
      {isEditing ? (
        <div className="bg-white dark:bg-zinc-800 rounded-lg shadow-md p-4 border border-gray-200 dark:border-zinc-700">
          <div className="flex items-start gap-4">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => onToggle(task.id)}
              className="mt-1 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <div className="flex-1 space-y-3">
              <input
                type="text"
                defaultValue={task.title}
                className="w-full text-lg font-semibold bg-transparent border-b border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    const newTitle = (e.target as HTMLInputElement).value;
                    onEdit(task.id, { title: newTitle });
                    setIsEditing(false);
                  } else if (e.key === 'Escape') {
                    setIsEditing(false);
                  }
                }}
              />

              <textarea
                defaultValue={task.description || ''}
                className="w-full bg-transparent border-b border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                rows={2}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && e.ctrlKey) {
                    const newDescription = (e.target as HTMLTextAreaElement).value;
                    onEdit(task.id, { description: newDescription });
                    setIsEditing(false);
                  } else if (e.key === 'Escape') {
                    setIsEditing(false);
                  }
                }}
              />

              {/* Advanced task features */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-3">
                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1">Priority</label>
                  <select
                    defaultValue={task.priority || 'medium'}
                    className="w-full text-sm bg-transparent border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    onChange={(e) => {
                      onEdit(task.id, { priority: e.target.value as 'low' | 'medium' | 'high' });
                    }}
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1">Category</label>
                  <input
                    type="text"
                    defaultValue={task.category || ''}
                    placeholder="Work, Personal, etc."
                    className="w-full text-sm bg-transparent border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    onBlur={(e) => {
                      onEdit(task.id, { category: e.target.value || undefined });
                    }}
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1">Due Date</label>
                  <input
                    type="date"
                    defaultValue={task.due_date?.split('T')[0] || ''}
                    className="w-full text-sm bg-transparent border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    onChange={(e) => {
                      onEdit(task.id, { due_date: e.target.value ? `${e.target.value}T00:00:00` : undefined });
                    }}
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-gray-500 mb-1">Reminder</label>
                  <input
                    type="datetime-local"
                    defaultValue={task.reminder_time?.substring(0, 16) || ''}
                    className="w-full text-sm bg-transparent border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    onChange={(e) => {
                      onEdit(task.id, { reminder_time: e.target.value ? `${e.target.value}:00` : undefined });
                    }}
                  />
                </div>
              </div>

              <div className="flex items-center gap-4 mt-2">
                <label className="flex items-center gap-2 text-sm">
                  <input
                    type="checkbox"
                    defaultChecked={!!task.is_recurring}
                    className="rounded"
                    onChange={(e) => {
                      onEdit(task.id, { is_recurring: e.target.checked });
                    }}
                  />
                  <span className="text-gray-700 dark:text-gray-300">Recurring</span>
                </label>

                {task.is_recurring && (
                  <div>
                    <label className="block text-xs font-medium text-gray-500 mb-1">Pattern</label>
                    <select
                      defaultValue={task.recurrence_pattern || ''}
                      className="text-sm bg-transparent border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      onChange={(e) => {
                        onEdit(task.id, { recurrence_pattern: e.target.value });
                      }}
                    >
                      <option value="">Select pattern</option>
                      <option value="daily">Daily</option>
                      <option value="weekly">Weekly</option>
                      <option value="monthly">Monthly</option>
                      <option value="yearly">Yearly</option>
                    </select>
                  </div>
                )}
              </div>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setIsEditing(false)}
                className="text-green-600 hover:text-green-800"
              >
                ✓
              </button>
              <button
                onClick={() => setIsEditing(false)}
                className="text-gray-600 hover:text-gray-800"
              >
                ✕
              </button>
            </div>
          </div>
        </div>
      ) : (
        <div className={`
          bg-white dark:bg-zinc-800 rounded-lg shadow-md p-4 border
          ${task.completed ? 'border-gray-200 opacity-75 dark:border-zinc-700' : 'border-l-4 border-l-blue-500'}
        `}>
          <div className="flex items-start gap-4">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => onToggle(task.id)}
              className="mt-1 h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />

            <div className="flex-1">
              <h3 className={`font-semibold ${task.completed ? 'line-through text-gray-500 dark:text-gray-500' : 'text-gray-800 dark:text-white'}`}>
                {task.title}
              </h3>
              {task.description && (
                <p className="text-gray-600 dark:text-gray-400 mt-1">{task.description}</p>
              )}

              <div className="mt-2 flex flex-wrap items-center gap-2">
                <span className={`
                  inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
                  ${task.priority === 'high' ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300' :
                    task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300' :
                      'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'}
                `}>
                  {(task.priority || 'medium').charAt(0).toUpperCase() + (task.priority || 'medium').slice(1)}
                </span>

                {task.category && (
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300">
                    {task.category}
                  </span>
                )}

                {task.due_date && (
                  <span className={`
                    inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
                    ${new Date(task.due_date) < new Date() && !task.completed ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300' :
                      new Date(task.due_date) < new Date(Date.now() + 86400000) && !task.completed ? 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-300' :
                      'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'}
                  `}>
                    📅 {new Date(task.due_date).toLocaleDateString()}
                  </span>
                )}

                {task.is_recurring && (
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300">
                    🔁 {task.recurrence_pattern || 'Recurring'}
                  </span>
                )}

                <span className="text-xs text-gray-500 dark:text-gray-400">
                  Created: {new Date(task.created_at).toLocaleDateString()}
                </span>
              </div>
            </div>

            <div className="flex gap-2">
              <button
                onClick={() => setIsEditing(true)}
                className="p-2 rounded-full bg-blue-100 text-blue-800 hover:bg-blue-200 dark:bg-blue-900/30 dark:text-blue-300"
                title="Edit task"
              >
                ✏️
              </button>
              <button
                onClick={() => setIsDeleteConfirmOpen(true)}
                className="p-2 rounded-full bg-red-100 text-red-800 hover:bg-red-200 dark:bg-red-900/30 dark:text-red-300"
                title="Delete task"
              >
                🗑️
              </button>
            </div>
          </div>
        </div>
      )}

      <ConfirmDialog
        isOpen={isDeleteConfirmOpen}
        title="Delete Task"
        message={`Are you sure you want to delete "${task.title}"? This action cannot be undone.`}
        onConfirm={handleDeleteConfirm}
        onCancel={() => setIsDeleteConfirmOpen(false)}
        variant="danger"
        confirmText="Delete"
        cancelText="Cancel"
      />
    </>
  );
}