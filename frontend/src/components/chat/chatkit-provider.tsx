'use client';

import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { useChat } from 'ai/react';
import { Message } from 'ai';

interface ChatContextType {
  messages: Message[];
  input: string;
  setInput: (input: string) => void;
  handleInputChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  handleSubmit: (e: React.FormEvent) => void;
  isLoading: boolean;
  addMessage: (message: Message) => void;
  clearMessages: () => void;
  errorOccurred: boolean;
  errorMessage: string;
  clearError: () => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const useChatKit = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChatKit must be used within a ChatKitProvider');
  }
  return context;
};

interface ChatKitProviderProps {
  children: ReactNode;
  userId: string;
  initialMessages?: Message[];
}

export const ChatKitProvider: React.FC<ChatKitProviderProps> = ({
  children,
  userId,
  initialMessages = []
}) => {
  // Add error state management
  const [errorOccurred, setErrorOccurred] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // Get token from common storage keys (robust version)
  const getAuthToken = () => {
    if (typeof window === 'undefined') return '';

    // Try localStorage first - CHECK better_auth_token FIRST (that's what auth-client stores!)
    let token = localStorage.getItem('better_auth_token') ||
      localStorage.getItem('better-auth.session_token') ||
      localStorage.getItem('auth_token');

    // If not in localStorage, try cookies
    if (!token && typeof document !== 'undefined') {
      const allCookies = document.cookie.split(';');
      const authCookie = allCookies.find(c =>
        c.trim().startsWith('better_auth_token=') ||
        c.trim().startsWith('better-auth.session_token=')
      );
      if (authCookie) {
        token = authCookie.trim().split('=')[1];
      }
    }

    return token || '';
  };

  // Load messages from localStorage on mount
  const loadMessagesFromStorage = (): Message[] => {
    if (typeof window === 'undefined') return [];

    try {
      const stored = localStorage.getItem(`chat-messages-${userId}`);
      if (stored) {
        const parsed = JSON.parse(stored);
        return parsed.map((msg: any) => ({
          ...msg,
          createdAt: new Date(msg.createdAt)
        }));
      }
    } catch (e) {
      console.error('Error loading messages from storage:', e);
    }
    return [];
  };

  // Save messages to localStorage whenever they change
  const saveMessagesToStorage = (messages: Message[]) => {
    if (typeof window === 'undefined') return;

    try {
      const serializableMessages = messages.map(({ createdAt, ...rest }) => ({
        ...rest,
        createdAt: createdAt instanceof Date ? createdAt.toISOString() : createdAt
      }));
      localStorage.setItem(`chat-messages-${userId}`, JSON.stringify(serializableMessages));
    } catch (e) {
      console.error('Error saving messages to storage:', e);
    }
  };

  const authToken = getAuthToken();
  if (typeof window !== 'undefined') {
    console.log('%c CHAT AUTH DEBUG ', 'background: #222; color: #bada55; font-size: 16px', {
      userId,
      tokenPresent: !!authToken,
      tokenStart: authToken ? authToken.substring(0, 10) + '...' : 'NONE'
    });
  }

  const {
    messages,
    input,
    handleInputChange,
    handleSubmit,
    setInput,
    isLoading,
    append,
    setMessages: originalSetMessages
  } = useChat({
    api: `/api/${userId}/chat`,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getAuthToken()}`,
    },
    body: {
      // Ensure the userId is also sent in the body as a backup
      userId: userId
    },
    onResponse: (response: any) => {
      console.log('%c CHAT RESPONSE ', 'background: #222; color: #ff00ff', {
        status: response.status,
        ok: response.ok,
        statusText: response.statusText
      });
      if (response.status === 401) {
        console.error('Chat error: 401 Unauthorized. The backend rejected your token.');
        // Set error state for display in UI
        setErrorOccurred(true);
        setErrorMessage('Authentication failed. Please sign in again.');
      } else if (response.status === 403) {
        console.error('Chat error: 403 Forbidden. Access to this resource is denied.');
        setErrorOccurred(true);
        setErrorMessage('Access denied. Please verify you have permission to access this resource.');
      }
    },
    onError: (error: any) => {
      console.error('%c CHAT ERROR ', 'background: #ff0000; color: #fff', error);

      // Set error state for display in UI
      setErrorOccurred(true);
      setErrorMessage(error.message || 'Failed to get response from AI service. The AI service may be temporarily unavailable.');
    }
  });

  // Update messages state with persistence
  useEffect(() => {
    // Load initial messages from storage if none exist yet
    if (messages.length === 0) {
      const storedMessages = loadMessagesFromStorage();
      if (storedMessages.length > 0) {
        originalSetMessages(storedMessages);
      }
    } else {
      // Save current messages to storage
      saveMessagesToStorage(messages);
    }
  }, [messages, originalSetMessages, userId]);

  const clearMessages = () => {
    originalSetMessages([]);
    // Clear from storage as well
    if (typeof window !== 'undefined') {
      localStorage.removeItem(`chat-messages-${userId}`);
    }
  };

  const clearError = () => {
    setErrorOccurred(false);
    setErrorMessage('');
  };

  const value = {
    messages,
    input,
    setInput,
    isLoading,
    handleInputChange,
    handleSubmit,
    addMessage: append,
    clearMessages,
    errorOccurred,
    errorMessage,
    clearError,
  };

  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};