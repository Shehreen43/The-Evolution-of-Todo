import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from 'axios';
import Cookies from 'js-cookie';
import {
  AuthResponse,
  SignInInput,
  SignUpInput,
  Task,
  ApiError,
  CreateTaskInput,
  UpdateTaskInput,
  User,
  TaskStatus,
  SortField,
  SortOrder
} from '@/types';

export type {
  Task,
  CreateTaskInput,
  UpdateTaskInput,
  SignUpInput,
  SignInInput,
  AuthResponse
};

// Aliases for compatibility with some components
export type TaskCreate = CreateTaskInput;
export type TaskUpdate = UpdateTaskInput;

class ApiClient {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 15000,
    });

    // Request Interceptor: Attach Token
    this.api.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        // For Better Auth integration, we'll use the stored Better Auth JWT token
        // Better Auth typically stores tokens in browser storage
        let token = null;

        // Look for Better Auth's standard token storage
        if (typeof window !== 'undefined') {
          // Better Auth typically stores tokens in localStorage with standard names
          token = localStorage.getItem('better-auth.session_token') ||
            localStorage.getItem('better_auth_token') ||
            localStorage.getItem('auth_token') ||
            Cookies.get('better-auth.session_token') ||
            Cookies.get('better_auth_token');

          // If no token found, try to extract from document.cookie manually
          if (!token) {
            const allCookies = document.cookie.split(';');
            const authCookie = allCookies.find(c =>
              c.trim().startsWith('better-auth.session_token=') ||
              c.trim().startsWith('better_auth_token=') ||
              c.trim().startsWith('authjs.session_token=')
            );
            if (authCookie) {
              token = authCookie.trim().split('=')[1];
            }
          }

          // Additional fallback: check for our custom token
          if (!token) {
            token = localStorage.getItem('better_auth_token');
          }
        }

        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response Interceptor: Error Handling
    this.api.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        // Handle 401 Unauthorized
        if (error.response?.status === 401) {
          if (typeof window !== 'undefined') {
            // Avoid redirect loops if already on auth pages
            if (!window.location.pathname.startsWith('/signin') &&
              !window.location.pathname.startsWith('/signup')) {
              // Clear any local tokens and cookies if present
              localStorage.removeItem('better_auth_token');
              Cookies.remove('better_auth_token');
              // Also remove the cookie via document.cookie
              document.cookie = 'better_auth_token=; path=/; max-age=0';
              window.location.href = `/signin?returnUrl=${encodeURIComponent(window.location.pathname)}`;
            }
          }
        }
        return Promise.reject(this.normalizeError(error));
      }
    );
  }

  private normalizeError(error: AxiosError): ApiError {
    const data = error.response?.data as ApiError | undefined;
    // Handle both FastAPI {detail: ...} and user-requested {message: ...}
    return {
      detail: data?.detail || error.message || 'An unexpected error occurred',
    };
  }


  // --- Token Management ---

  // Store Better Auth token when available
  public setBetterAuthToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('better_auth_token', token);
      Cookies.set('better_auth_token', token, { expires: 7, path: '/' });
    }
  }

  // --- Auth Endpoints ---

  /**
   * Get current user profile information
   */
  public async getCurrentUser(): Promise<User> {
    const response = await this.api.get<User>('/api/auth/me');
    return response.data;
  }

  /**
   * Logout user by clearing local token
   */
  public async logout(): Promise<void> {
    try {
      await this.api.post('/api/auth/logout');
    } finally {
      // Clear stored tokens and cookies
      if (typeof window !== 'undefined') {
        localStorage.removeItem('better_auth_token');
        Cookies.remove('better_auth_token');
        // Also remove the cookie via document.cookie
        document.cookie = 'better_auth_token=; path=/; max-age=0';
      }
    }
  }

  // --- Task Endpoints ---

  /**
   * Fetch all tasks for a specific user with optional filtering
   */
  public async getTasks(userId: string, params?: {
    status?: TaskStatus;
    sort?: SortField;
    order?: SortOrder;
    category?: string;
    due_date_filter?: string;
    is_recurring?: boolean;
    priority?: 'low' | 'medium' | 'high';
  }): Promise<Task[]> {
    const response = await this.api.get<Task[]>(`/api/${userId}/tasks`, { params });
    return response.data;
  }

  /**
   * Get a single task by ID
   */
  public async getTask(userId: string, taskId: number): Promise<Task> {
    const response = await this.api.get<Task>(`/api/${userId}/tasks/${taskId}`);
    return response.data;
  }

  /**
   * Create a new task
   */
  public async createTask(userId: string, data: CreateTaskInput): Promise<Task> {
    const response = await this.api.post<Task>(`/api/${userId}/tasks`, data);
    return response.data;
  }

  /**
   * Update an existing task
   */
  public async updateTask(userId: string, taskId: number, data: UpdateTaskInput): Promise<Task> {
    const response = await this.api.put<Task>(`/api/${userId}/tasks/${taskId}`, data);
    return response.data;
  }

  /**
   * Delete a task
   */
  public async deleteTask(userId: string, taskId: number): Promise<void> {
    await this.api.delete(`/api/${userId}/tasks/${taskId}`);
  }

  /**
   * Toggle task completion status
   */
  public async toggleComplete(userId: string, taskId: number): Promise<Task> {
    const response = await this.api.patch<Task>(`/api/${userId}/tasks/${taskId}/complete`);
    return response.data;
  }

  // --- Chat Endpoints ---

  /**
   * Send a message to the AI chatbot
   */
  public async sendMessage(userId: string, message: string, conversationId: number | null = null): Promise<{
    conversation_id: number;
    response: string;
    tool_calls?: Array<{
      tool: string;
      arguments: Record<string, any>;
      result: any;
    }>;
  }> {
    const response = await this.api.post<{
      conversation_id: number;
      response: string;
      tool_calls?: Array<{
        tool: string;
        arguments: Record<string, any>;
        result: any;
      }>;
    }>(`/api/${userId}/chat`, {
      message,
      conversation_id: conversationId
    });
    return response.data;
  }

  /**
   * Get list of user's conversations
   */
  public async getConversations(userId: string): Promise<Array<{
    id: number;
    user_id: string;
    title: string;
    created_at: string;
    updated_at: string;
  }>> {
    const response = await this.api.get<Array<{
      id: number;
      user_id: string;
      title: string;
      created_at: string;
      updated_at: string;
    }>>(`/api/${userId}/conversations`);
    return response.data;
  }

  /**
   * Get messages for a specific conversation
   */
  public async getConversationMessages(userId: string, conversationId: number): Promise<Array<{
    id: number;
    conversation_id: number;
    user_id: string;
    role: string;
    content: string;
    tool_calls?: string | null;
    created_at: string;
  }>> {
    const response = await this.api.get<Array<{
      id: number;
      conversation_id: number;
      user_id: string;
      role: string;
      content: string;
      tool_calls?: string | null;
      created_at: string;
    }>>(`/api/${userId}/conversations/${conversationId}/messages`);
    return response.data;
  }

  // --- Planning Endpoints ---

  /**
   * Generate an execution plan for a complex prompt
   */
  public async getPlan(userId: string, prompt: string): Promise<{
    plan: Array<{
      step: string;
      description: string;
      tool: string;
      arguments: Record<string, any>;
    }>;
  }> {
    const response = await this.api.post<{
      plan: Array<{
        step: string;
        description: string;
        tool: string;
        arguments: Record<string, any>;
      }>;
    }>(`/api/${userId}/chat/plan`, { prompt });
    return response.data;
  }

  // --- Voice Endpoints ---

  /**
   * Transcribe audio to text
   */
  public async transcribeAudio(userId: string, audioBlob: Blob): Promise<{ text: string }> {
    const formData = new FormData();
    formData.append('file', audioBlob, 'audio.wav');

    const response = await this.api.post<{ text: string }>(
      `/api/${userId}/audio/transcribe`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  }

  /**
   * Synthesize speech from text
   */
  public async synthesizeSpeech(userId: string, text: string, language: 'en' | 'ur' = 'en'): Promise<Blob> {
    const response = await this.api.post(
      `/api/${userId}/audio/speak`,
      { text, language },
      { responseType: 'blob' }
    );
    return response.data;
  }
}

// Export singleton instance
export const api = new ApiClient();
