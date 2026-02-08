export interface User {
    id: string;
    email: string;
    name: string;
    createdAt?: string; // Optional as it might not be needed in all UI contexts
    updatedAt?: string;
    emailVerified?: boolean; // For future phase compatibility
    image?: string;
}

export interface Task {
    id: number;
    user_id: string; // Backend sends snake_case 'user_id'
    title: string;
    description?: string;
    completed: boolean;
    priority?: 'low' | 'medium' | 'high'; // Added based on backend schema
    created_at: string; // Backend sends snake_case 'created_at'
    updated_at: string; // Backend sends snake_case 'updated_at'
    // Advanced task features
    due_date?: string;           // ISO string format
    reminder_time?: string;      // ISO string format
    category?: string;
    is_recurring?: boolean;
    recurrence_pattern?: string; // daily, weekly, monthly, yearly
    next_occurrence?: string;    // ISO string format
    end_recurrence?: string;     // ISO string format
    parent_task_id?: number;
}

export interface CreateTaskInput {
    title: string;
    description?: string;
    priority?: 'low' | 'medium' | 'high';
    // Advanced task features
    due_date?: string;           // ISO string format
    reminder_time?: string;      // ISO string format
    category?: string;
    is_recurring?: boolean;
    recurrence_pattern?: string; // daily, weekly, monthly, yearly
    end_recurrence?: string;     // ISO string format
}

export interface UpdateTaskInput {
    title?: string;
    description?: string;
    completed?: boolean;
    priority?: 'low' | 'medium' | 'high';
    // Advanced task features
    due_date?: string;           // ISO string format
    reminder_time?: string;      // ISO string format
    category?: string;
    is_recurring?: boolean;
    recurrence_pattern?: string; // daily, weekly, monthly, yearly
    end_recurrence?: string;     // ISO string format
}

export interface SignUpInput {
    name: string;
    email: string;
    password: string;
    // confirmPassword handled in frontend validation, not sent to API
}

export interface SignInInput {
    email: string;
    password: string;
}

export interface AuthResponse {
    user: User;
    token: string;
    expires_at: string;
}

export interface ApiError {
    detail: string; // FastAPI default error structure
}

export type TaskStatus = 'all' | 'pending' | 'completed';
export type SortField = 'created_at' | 'title' | 'updated_at' | 'due_date';
export type SortOrder = 'asc' | 'desc';
