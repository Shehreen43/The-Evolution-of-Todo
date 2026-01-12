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
            <div className="flex-1">
              <input
                type="text"
                defaultValue={task.title}
                className="w-full text-lg font-semibold bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500"
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
                className="w-full mt-2 bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-blue-500"
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
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => {
                  const titleInput = document.querySelector<HTMLInputElement>('input[value="' + task.title + '"]');
                  const descInput = document.querySelector<HTMLTextAreaElement>('textarea[value="' + (task.description || '') + '"]');
                  if (titleInput && descInput) {
                    onEdit(task.id, {
                      title: titleInput.value,
                      description: descInput.value || undefined
                    });
                  }
                  setIsEditing(false);
                }}
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

              <div className="mt-2 flex items-center gap-4">
                <span className={`
                  inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
                  ${task.priority === 'high' ? 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300' :
                    task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300' :
                    'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'}
                `}>
                  {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                </span>
                <span className="text-xs text-gray-500 dark:text-gray-400">
                  {new Date(task.created_at).toLocaleDateString()}
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