'use client';

import React from 'react';
import { useSession } from '@/lib/auth-client';
import { useTasks } from '@/hooks/useTasks';
import { TaskForm } from '@/components/tasks/task-form';
import { Button } from '@/components/ui';
import { CreateTaskInput } from '@/types';
import { ArrowLeft, PlusCircle } from 'lucide-react';
import Link from 'next/link';

export default function NewTaskPage() {
  const { data: session } = useSession();
  const { createTask, isLoading } = useTasks(session?.user?.id);

  const handleSubmit = async (data: CreateTaskInput) => {
    if (session?.user?.id) {
      await createTask(data);
      // Redirect to tasks page after successful creation
      window.location.href = '/tasks';
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <Link href="/tasks" className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors">
          <ArrowLeft className="h-5 w-5" />
          <span>Back to Tasks</span>
        </Link>
        <h1 className="text-3xl font-bold tracking-tight text-gray-900 font-outfit flex items-center gap-2">
          <PlusCircle className="h-8 w-8 text-emerald-600" />
          Create New Task
        </h1>
      </div>

      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-emerald-50 to-cyan-50 p-8 border border-emerald-100">
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-500 to-cyan-500"></div>

        <div className="relative z-10">
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Add Your Task</h2>
            <p className="text-gray-600">
              Create a new task with all the advanced features you need
            </p>
          </div>

          <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
            <TaskForm
              initialData={undefined}
              onCancel={() => window.location.href = '/tasks'}
              onSubmit={handleSubmit}
              isLoading={isLoading}
            />
          </div>
        </div>

        {/* Decorative elements */}
        <div className="absolute -top-10 -right-10 w-32 h-32 bg-emerald-200/30 rounded-full blur-xl"></div>
        <div className="absolute -bottom-10 -left-10 w-32 h-32 bg-cyan-200/30 rounded-full blur-xl"></div>
      </div>
    </div>
  );
}