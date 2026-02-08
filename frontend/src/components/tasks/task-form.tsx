import * as React from 'react';
import { useForm, useWatch } from 'react-hook-form';
import type { Resolver } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Task } from '@/types';
import { Input, Textarea, Button } from '@/components/ui';
import { cn } from '@/lib/utils';
import { RefreshCw, Calendar, Bell, ListTodo, Tag, AlignLeft, X } from 'lucide-react';

/* ---------------- Schema ---------------- */

const taskSchema = z
  .object({
    title: z.string().min(1, 'Title is required').max(200, 'Title too long'),
    description: z.string().max(1000, 'Description too long').optional().or(z.literal('')),
    priority: z.enum(['low', 'medium', 'high']).default('medium'),

    due_date: z.string().optional().or(z.literal('')),
    reminder_time: z.string().optional().or(z.literal('')),

    category: z.string().max(50, 'Category too long').optional().or(z.literal('')),

    is_recurring: z.boolean().default(false),
    recurrence_pattern: z.enum(['daily', 'weekly', 'monthly', 'yearly']).optional(),
    end_recurrence: z.string().optional().or(z.literal('')),
  })
  .superRefine((data, ctx) => {
    if (data.is_recurring && !data.recurrence_pattern) {
      ctx.addIssue({
        path: ['recurrence_pattern'],
        message: 'Recurrence pattern is required for recurring tasks',
        code: z.ZodIssueCode.custom,
      });
    }
  });

type TaskFormData = z.infer<typeof taskSchema>;

/* ---------------- Props ---------------- */

interface TaskFormProps {
  initialData?: Task;
  onSubmit: (data: TaskFormData) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
}

/* ---------------- Component ---------------- */

export function TaskForm({
  initialData,
  onSubmit,
  onCancel,
  isLoading,
}: TaskFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    control,
  } = useForm<TaskFormData>({
    // cast resolver to match the useForm generic type
    resolver: zodResolver(taskSchema) as unknown as Resolver<TaskFormData>,
    defaultValues: {
      title: initialData?.title ?? '',
      description: initialData?.description ?? '',
      priority: initialData?.priority ?? 'medium',
      due_date: initialData?.due_date ?? '',
      reminder_time: initialData?.reminder_time ?? '',
      category: initialData?.category ?? '',
      is_recurring: initialData?.is_recurring ?? false,
      recurrence_pattern: ['daily', 'weekly', 'monthly', 'yearly'].includes(initialData?.recurrence_pattern ?? '')
        ? (initialData?.recurrence_pattern as 'daily' | 'weekly' | 'monthly' | 'yearly')
        : undefined,
      end_recurrence: initialData?.end_recurrence ?? '',
    },
  });

  const titleValue = useWatch({ control, name: 'title' }) ?? '';
  const descriptionValue = useWatch({ control, name: 'description' }) ?? '';
  const isRecurring = useWatch({ control, name: 'is_recurring' }) ?? false;

  const onSubmitForm = async (data: TaskFormData) => {
    try {
      await onSubmit(data);
    } catch (error) {
      console.error('Form submission error:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmitForm)} className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Task Title *
        </label>
        <div className="relative">
          <input
            type="text"
            placeholder="What needs to be done?"
            className={cn(
              'w-full px-4 py-3 pl-12 rounded-xl border border-emerald-300 bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
              'dark:bg-emerald-800 dark:border-emerald-700 dark:text-white',
              errors.title && 'border-red-500 focus:ring-red-500'
            )}
            {...register('title')}
          />
          <ListTodo className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400 dark:text-gray-500" />
        </div>
        <div className="flex justify-between items-center mt-1">
          {errors.title && (
            <p className="text-sm text-red-500 dark:text-red-400">
              {errors.title.message}
            </p>
          )}
          <p className="text-xs text-gray-500 dark:text-gray-400 ml-auto">
            {titleValue.length}/200
          </p>
        </div>
      </div>

      {/* Priority & Category */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Priority
          </label>
          <div className="flex gap-2">
            {(['low', 'medium', 'high'] as const).map((p) => (
              <label key={p} className="flex-1">
                <input
                  type="radio"
                  value={p}
                  className="peer sr-only"
                  {...register('priority')}
                />
                <span
                  className={cn(
                    'flex items-center justify-center px-4 py-3 rounded-xl border text-sm font-medium transition-all cursor-pointer',
                    'peer-checked:ring-2 peer-checked:ring-emerald-500 peer-checked:border-emerald-500',
                    p === 'high'
                      ? 'peer-checked:bg-red-500 peer-checked:text-white bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-200'
                      : p === 'medium'
                        ? 'peer-checked:bg-emerald-500 peer-checked:text-white bg-emerald-50 dark:bg-emerald-900/20 text-emerald-800 dark:text-emerald-200'
                        : 'peer-checked:bg-emerald-500 peer-checked:text-white bg-emerald-50 dark:bg-emerald-900/20 text-emerald-800 dark:text-emerald-200',
                    'hover:bg-emerald-50 dark:hover:bg-emerald-50'
                  )}
                >
                  {p.charAt(0).toUpperCase() + p.slice(1)}
                </span>
              </label>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Category
          </label>
          <div className="relative">
            <input
              type="text"
              placeholder="Work, Personal, Shopping, etc."
              className={cn(
                'w-full px-4 py-3 pl-10 rounded-xl border border-gray-300 bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
                'dark:bg-gray-800 dark:border-gray-700 dark:text-white',
                errors.category && 'border-red-500 focus:ring-red-500'
              )}
              {...register('category')}
            />
            <Tag className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400 dark:text-gray-500" />
          </div>
          {errors.category && (
            <p className="mt-1 text-sm text-red-500 dark:text-red-400">
              {errors.category.message}
            </p>
          )}
        </div>
      </div>

      {/* Dates */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Due Date
          </label>
          <div className="relative">
            <input
              type="date"
              className={cn(
                'w-full px-4 py-3 pl-10 rounded-xl border border-gray-300 bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
                'dark:bg-gray-800 dark:border-gray-700 dark:text-white',
                errors.due_date && 'border-red-500 focus:ring-red-500'
              )}
              {...register('due_date')}
            />
            <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400 dark:text-gray-500" />
          </div>
          {errors.due_date && (
            <p className="mt-1 text-sm text-red-500 dark:text-red-400">
              {errors.due_date.message}
            </p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Reminder Time
          </label>
          <div className="relative">
            <input
              type="datetime-local"
              className={cn(
                'w-full px-4 py-3 pl-10 rounded-xl border border-gray-300 bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
                'dark:bg-gray-800 dark:border-gray-700 dark:text-white',
                errors.reminder_time && 'border-red-500 focus:ring-red-500'
              )}
              {...register('reminder_time')}
            />
            <Bell className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400 dark:text-gray-500" />
          </div>
          {errors.reminder_time && (
            <p className="mt-1 text-sm text-red-500 dark:text-red-400">
              {errors.reminder_time.message}
            </p>
          )}
        </div>
      </div>

      {/* Recurring */}
      <div className="space-y-4">
        <div className="flex items-center justify-between p-4 rounded-xl border bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-emerald-100 dark:bg-emerald-900/30 rounded-lg">
              <RefreshCw className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
            </div>
            <div>
              <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Recurring Task</label>
              <p className="text-xs text-gray-500 dark:text-gray-400">Set up automatic repetitions</p>
            </div>
          </div>

          <label className="relative inline-flex items-center cursor-pointer">
            <input
              type="checkbox"
              className="sr-only peer"
              {...register('is_recurring')}
            />
            <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-emerald-300 dark:peer-focus:ring-emerald-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-emerald-600"></div>
          </label>
        </div>

        {isRecurring && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 ml-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Recurrence Pattern
              </label>
              <select
                className={cn(
                  'w-full px-4 py-3 rounded-xl border border-gray-300 bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
                  'dark:bg-gray-800 dark:border-gray-700 dark:text-white',
                  errors.recurrence_pattern && 'border-red-500 focus:ring-red-500'
                )}
                {...register('recurrence_pattern')}
              >
                <option value="">Select pattern</option>
                <option value="daily">Daily</option>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
                <option value="yearly">Yearly</option>
              </select>
              {errors.recurrence_pattern && (
                <p className="mt-1 text-sm text-red-500 dark:text-red-400">
                  {errors.recurrence_pattern.message}
                </p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                End Recurrence
              </label>
              <div className="relative">
                <input
                  type="date"
                  className={cn(
                    'w-full px-4 py-3 pl-10 rounded-xl border border-gray-300 bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all',
                    'dark:bg-gray-800 dark:border-gray-700 dark:text-white',
                    errors.end_recurrence && 'border-red-500 focus:ring-red-500'
                  )}
                  {...register('end_recurrence')}
                />
                <X className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400 dark:text-gray-500" />
              </div>
              {errors.end_recurrence && (
                <p className="mt-1 text-sm text-red-500 dark:text-red-400">
                  {errors.end_recurrence.message}
                </p>
              )}
            </div>
          </div>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Description (Optional)
        </label>
        <div className="relative">
          <textarea
            placeholder="Add more details..."
            rows={4}
            className={cn(
              'w-full px-4 py-3 pl-10 rounded-xl border border-gray-300 bg-white text-gray-900 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition-all resize-none',
              'dark:bg-gray-800 dark:border-gray-700 dark:text-white',
              errors.description && 'border-red-500 focus:ring-red-500'
            )}
            {...register('description')}
          ></textarea>
          <AlignLeft className="absolute left-3 top-3 h-5 w-5 text-gray-400 dark:text-gray-500" />
        </div>
        <div className="flex justify-between items-center mt-1">
          {errors.description && (
            <p className="text-sm text-red-500 dark:text-red-400">
              {errors.description.message}
            </p>
          )}
          <p className="text-xs text-gray-500 dark:text-gray-400 ml-auto">
            {descriptionValue.length}/1000
          </p>
        </div>
      </div>

      <div className="flex justify-end gap-3 pt-4">
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          className="rounded-xl px-6"
        >
          Cancel
        </Button>
        <Button
          type="submit"
          isLoading={isLoading}
          className="rounded-xl px-6 bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-600 hover:to-cyan-600 shadow-md hover:shadow-lg transition-all"
        >
          {initialData ? 'Update Task' : 'Create Task'}
        </Button>
      </div>
    </form>
  );
}
