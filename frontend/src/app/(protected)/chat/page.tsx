'use client';

import React from 'react';
import { ChatKitInterface } from '@/components/chat/chatkit-component';
import { ChatKitProvider } from '@/components/chat/chatkit-provider';
import { useSession } from '@/lib/auth-client';
import { Sparkles, User, ArrowRight } from 'lucide-react';
import Link from 'next/link';


export default function ChatPage() {
  const { data: session } = useSession();

  if (!session?.user?.id) {
    return (
      <div className="max-w-4xl mx-auto space-y-8 px-4 py-8">
        <div className="text-center">
          <div className="inline-flex items-center justify-center p-3 bg-gradient-to-br from-emerald-500 to-cyan-500 rounded-2xl mb-6">
            <Sparkles className="h-8 w-8 text-white" />
          </div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-emerald-600 to-cyan-600 bg-clip-text text-transparent mb-4">
            AI Todo Assistant
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
            Please sign in to access the AI assistant and start managing your tasks with intelligent help.
          </p>
        </div>

        <div className="bg-gradient-to-br from-gray-50 to-white dark:from-gray-800 dark:to-gray-900 rounded-3xl p-8 border border-gray-200 dark:border-gray-700 shadow-lg">
          <div className="text-center">
            <div className="mx-auto h-24 w-24 rounded-full bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-800 flex items-center justify-center mb-6">
              <User className="h-12 w-12 text-gray-400 dark:text-gray-500" />
            </div>
            <p className="text-gray-500 dark:text-gray-400 mb-6">
              Sign in to unlock the AI-powered task management experience
            </p>
            <Link href="/signin" className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-emerald-500 to-cyan-500 text-white rounded-xl font-medium shadow-sm hover:shadow-md transition-all duration-200 hover:scale-105">
              Sign In
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50 dark:bg-gray-900">
      <ChatKitProvider userId={session.user.id}>
        <ChatKitInterface />
      </ChatKitProvider>
    </div>
  );
}