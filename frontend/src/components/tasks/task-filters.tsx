'use client';

import * as React from 'react';
import { TaskStatus, SortField, SortOrder } from '@/types';
import { cn } from '@/lib/utils';
import { Filter, SortAsc, SortDesc, Calendar, Tag } from 'lucide-react';

interface TaskFiltersProps {
    currentStatus: TaskStatus;
    onStatusChange: (status: TaskStatus) => void;
    currentSort: SortField;
    onSortChange: (sort: SortField) => void;
    currentOrder: SortOrder;
    onOrderChange: (order: SortOrder) => void;
    currentCategory?: string;
    onCategoryChange?: (category: string) => void;
    currentDueDateFilter?: string;
    onDueDateFilterChange?: (filter: string) => void;
    currentRecurringFilter?: boolean | 'all';
    onRecurringFilterChange?: (filter: boolean | 'all') => void;
}

export function TaskFilters({
    currentStatus,
    onStatusChange,
    currentSort,
    onSortChange,
    currentOrder,
    onOrderChange,
    currentCategory = '',
    onCategoryChange,
    currentDueDateFilter = '',
    onDueDateFilterChange,
    currentRecurringFilter = 'all',
    onRecurringFilterChange,
}: TaskFiltersProps) {
    const statuses: { label: string; value: TaskStatus }[] = [
        { label: 'All', value: 'all' },
        { label: 'Pending', value: 'pending' },
        { label: 'Completed', value: 'completed' },
    ];

    const recurringOptions = [
        { label: 'All', value: 'all' },
        { label: 'Recurring', value: true },
        { label: 'Non-recurring', value: false },
    ];

    const dueDateOptions = [
        { label: 'All', value: '' },
        { label: 'Due Today', value: 'today' },
        { label: 'Overdue', value: 'overdue' },
        { label: 'Due This Week', value: 'week' },
        { label: 'Due This Month', value: 'month' },
    ];

    return (
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between rounded-3xl border border-gray-100 bg-white p-4 shadow-sm">
            <div className="flex flex-wrap items-center gap-2 overflow-x-auto pb-2 md:pb-0 no-scrollbar">
                {statuses.map((s) => (
                    <button
                        key={s.value}
                        onClick={() => onStatusChange(s.value)}
                        className={cn(
                            "whitespace-nowrap rounded-2xl px-5 py-2 text-sm font-bold transition-all",
                            currentStatus === s.value
                                ? "bg-emerald-600 text-white shadow-md shadow-emerald-200"
                                : "text-gray-500 hover:bg-emerald-50 hover:text-emerald-700"
                        )}
                    >
                        {s.label}
                    </button>
                ))}

                {/* Category filter */}
                <div className="flex items-center gap-2 pl-2">
                    <Tag className="h-4 w-4 text-gray-400" />
                    <select
                        value={currentCategory}
                        onChange={(e) => onCategoryChange?.(e.target.value)}
                        className="rounded-xl border-gray-100 bg-emerald-50/50 px-3 py-2 text-sm font-bold text-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 min-w-[120px]"
                    >
                        <option value="">All Categories</option>
                        <option value="work">Work</option>
                        <option value="personal">Personal</option>
                        <option value="shopping">Shopping</option>
                        <option value="health">Health</option>
                        <option value="education">Education</option>
                    </select>
                </div>

                {/* Due date filter */}
                <div className="flex items-center gap-2 pl-2">
                    <Calendar className="h-4 w-4 text-gray-400" />
                    <select
                        value={currentDueDateFilter}
                        onChange={(e) => onDueDateFilterChange?.(e.target.value)}
                        className="rounded-xl border-gray-100 bg-emerald-50/50 px-3 py-2 text-sm font-bold text-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 min-w-[140px]"
                    >
                        {dueDateOptions.map(option => (
                            <option key={option.value} value={option.value}>{option.label}</option>
                        ))}
                    </select>
                </div>

                {/* Recurring filter */}
                <div className="flex items-center gap-2 pl-2">
                    <select
                        value={currentRecurringFilter === 'all' ? 'all' : String(currentRecurringFilter)}
                        onChange={(e) => onRecurringFilterChange?.(e.target.value === 'all' ? 'all' : e.target.value === 'true')}
                        className="rounded-xl border-gray-100 bg-emerald-50/50 px-3 py-2 text-sm font-bold text-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 min-w-[140px]"
                    >
                        {recurringOptions.map(option => (
                            <option key={String(option.value)} value={String(option.value)}>{option.label}</option>
                        ))}
                    </select>
                </div>
            </div>

            <div className="flex items-center gap-3 border-t pt-4 md:border-t-0 md:pt-0">
                <div className="flex items-center gap-2 text-sm font-bold text-gray-400">
                    <Filter className="h-4 w-4" />
                    <span>Sort by</span>
                </div>

                <select
                    value={currentSort}
                    onChange={(e) => onSortChange(e.target.value as SortField)}
                    className="rounded-xl border-gray-100 bg-emerald-50/50 px-3 py-2 text-sm font-bold text-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                >
                    <option value="created_at">Date Created</option>
                    <option value="title">Title</option>
                    <option value="updated_at">Last Updated</option>
                    <option value="due_date">Due Date</option>
                    <option value="priority">Priority</option>
                </select>

                <button
                    onClick={() => onOrderChange(currentOrder === 'asc' ? 'desc' : 'asc')}
                    className="rounded-xl bg-emerald-50 p-2 text-emerald-700 hover:bg-emerald-100 transition-all active:scale-95"
                    title={currentOrder === 'asc' ? 'Ascending' : 'Descending'}
                >
                    {currentOrder === 'asc' ? <SortAsc className="h-5 w-5" /> : <SortDesc className="h-5 w-5" />}
                </button>
            </div>
        </div>
    );
}
