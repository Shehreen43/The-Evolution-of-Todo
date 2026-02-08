'use client';

import { useEffect, useRef } from 'react';
import { Task } from '@/types';

/**
 * Custom hook to handle browser notifications for task reminders
 */
export function useReminderNotifications(tasks: Task[]) {
  const scheduledReminders = useRef<Map<number, number>>(new Map()); // taskId -> timeoutId

  useEffect(() => {
    // Request notification permission if not already granted
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission();
    }

    // Clear any existing reminders to prevent duplicates
    scheduledReminders.current.forEach((timeoutId, taskId) => {
      clearTimeout(timeoutId);
    });
    scheduledReminders.current.clear();

    // Schedule reminders for tasks that have future reminder times
    tasks.forEach(task => {
      if (task.reminder_time && !task.completed) {
        const reminderTime = new Date(task.reminder_time).getTime();
        const currentTime = Date.now();
        const timeDiff = reminderTime - currentTime;

        // Only schedule if the reminder is in the future
        if (timeDiff > 0) {
          const timeoutId = window.setTimeout(() => {
            if (Notification.permission === 'granted') {
              new Notification('Task Reminder ⏰', {
                body: task.title,
                icon: '/favicon.ico',
                tag: `task-${task.id}`,
              });
            }
            // Remove from scheduled reminders after triggering
            scheduledReminders.current.delete(task.id);
          }, timeDiff);

          // Store the timeout ID to allow for cleanup
          scheduledReminders.current.set(task.id, timeoutId);
        }
      }
    });

    // Cleanup on unmount
    return () => {
      scheduledReminders.current.forEach((timeoutId, taskId) => {
        clearTimeout(timeoutId);
      });
      scheduledReminders.current.clear();
    };
  }, [tasks]);

  // Function to clear a specific reminder if needed
  const clearReminder = (taskId: number) => {
    const timeoutId = scheduledReminders.current.get(taskId);
    if (timeoutId) {
      clearTimeout(timeoutId);
      scheduledReminders.current.delete(taskId);
    }
  };

  return { clearReminder };
}