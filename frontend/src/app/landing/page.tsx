'use client';

import Link from 'next/link';

export default function LandingPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black p-4">
      <div className="flex flex-col items-center gap-6 p-8 text-center">
        <h1 className="text-3xl font-bold text-gray-800 dark:text-white">The Evolution of Todo</h1>
        <p className="text-lg text-gray-600 dark:text-gray-300">
          A full-featured todo application with authentication and task management
        </p>
        <div className="flex gap-4">
          <Link
            href="/signup"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Get Started
          </Link>
          <Link
            href="/signin"
            className="border border-gray-300 text-gray-700 px-6 py-3 rounded-lg hover:bg-gray-100 transition-colors dark:border-zinc-600 dark:text-gray-300 dark:hover:bg-zinc-800"
          >
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}