'use client';

import React, { useEffect, useRef, useState, useCallback } from 'react';
import { useChatKit } from './chatkit-provider';
import { useVoice } from '@/hooks/useVoice';
import { usePlanning } from '@/hooks/usePlanning';
import { PlanningSteps } from './planning-steps';
import { Button } from '@/components/ui';
import {
  Send,
  Mic,
  MicOff,
  Loader2,
  User,
  Bot,
  Eraser,
  Sparkles,
  Trash2,
  History,
  X
} from 'lucide-react';
import { cn } from '@/lib/utils';

export const ChatKitInterface: React.FC = () => {
  const {
    messages,
    input,
    handleInputChange,
    handleSubmit,
    isLoading,
    clearMessages,
    errorOccurred,
    errorMessage,
    clearError
  } = useChatKit();

  const { isListening, startListening, stopListening, transcript } = useVoice();
  const { plan, currentStepIndex } = usePlanning();

  const [showHistoryModal, setShowHistoryModal] = useState(false);
  const [selectedHistory, setSelectedHistory] = useState<any>(null);

  const scrollRef = useRef<HTMLDivElement>(null);

  /* Auto-scroll */
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  /* Sync voice transcript to input */
  useEffect(() => {
    if (!transcript) return;

    const event = {
      target: { value: transcript }
    } as React.ChangeEvent<HTMLTextAreaElement>;

    handleInputChange(event);
  }, [transcript, handleInputChange]);

  const handleFormSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    if (errorOccurred) {
      clearError();
    }

    handleSubmit(e);
  };

  const toggleVoice = () => {
    isListening ? stopListening() : startListening();
  };

  /* ---------------- Chat History ---------------- */

  const saveConversationToHistory = useCallback(() => {
    if (messages.length === 0) return;

    const history = JSON.parse(localStorage.getItem('chatHistory') || '[]');

    history.unshift({
      id: Date.now(),
      timestamp: new Date().toISOString(),
      title: messages[0]?.content?.slice(0, 30) + '...' || 'New Conversation',
      messages,
      wordCount: messages.reduce(
        (acc, m) => acc + (m.content?.split(' ').length || 0),
        0
      )
    });

    localStorage.setItem('chatHistory', JSON.stringify(history.slice(0, 10)));
  }, [messages]);

  useEffect(() => {
    const timer = setTimeout(saveConversationToHistory, 2000);
    return () => clearTimeout(timer);
  }, [messages, saveConversationToHistory]);

  const loadAllHistory = () => {
    const history = JSON.parse(localStorage.getItem('chatHistory') || '[]');
    setSelectedHistory(history);
    setShowHistoryModal(true);
  };

  const deleteConversationFromHistory = (id: number) => {
    const history = JSON.parse(localStorage.getItem('chatHistory') || '[]');
    localStorage.setItem(
      'chatHistory',
      JSON.stringify(history.filter((h: any) => h.id !== id))
    );
  };

  const clearAllHistory = () => {
    localStorage.removeItem('chatHistory');
  };

  const [sidebarOpen, setSidebarOpen] = useState(true);

  /* ---------------- Render ---------------- */

  return (
    <div className="flex h-full bg-gray-50 dark:bg-gray-900">
      {/* Sidebar */}
      <div className={`bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 transition-all duration-300 ${sidebarOpen ? 'w-64' : 'w-0'} flex flex-col`}>
        <div className="p-4 border-b border-gray-200 dark:border-gray-700">
          <div className="flex items-center justify-between">
            <Button
              variant="outline"
              size="sm"
              className="flex-1 bg-gradient-to-r from-emerald-500 to-cyan-500 text-white hover:from-emerald-600 hover:to-cyan-600"
              onClick={() => {
                clearMessages();
                saveConversationToHistory();
              }}
            >
              <Sparkles className="h-4 w-4 mr-2" />
              New Chat
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="ml-2"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-2">
          <div className="space-y-1">
            {JSON.parse(localStorage.getItem('chatHistory') || '[]').map((chat: any) => (
              <div
                key={chat.id}
                className="p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer flex items-center justify-between"
                onClick={() => {
                  // Load the chat
                  setSelectedHistory(chat.messages);
                }}
              >
                <div className="truncate text-sm text-gray-800 dark:text-gray-200">
                  {chat.title}
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteConversationFromHistory(chat.id);
                  }}
                  className="h-6 w-6 p-0 text-gray-500 hover:text-red-500"
                >
                  <X className="h-3 w-3" />
                </Button>
              </div>
            ))}
          </div>
        </div>

        <div className="p-4 border-t border-gray-200 dark:border-gray-700">
          <div className="flex items-center space-x-3">
            <div className="h-8 w-8 rounded-full bg-gradient-to-br from-emerald-500 to-cyan-500 flex items-center justify-center">
              <User className="h-4 w-4 text-white" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                {localStorage.getItem('user_name') || 'User'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className={`flex-1 flex flex-col ${sidebarOpen ? 'ml-0' : ''}`}>
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
          {!sidebarOpen && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setSidebarOpen(true)}
              className="mr-2"
            >
              <Sparkles className="h-4 w-4" />
            </Button>
          )}
          <div className="flex items-center space-x-3">
            <div className="p-2.5 bg-gradient-to-br from-emerald-500 to-cyan-500 rounded-xl shadow-sm">
              <Sparkles className="h-5 w-5 text-white" />
            </div>
            <div>
              <h2 className="text-base font-semibold text-gray-900 dark:text-white">AI Assistant</h2>
              <p className="text-xs text-emerald-600 dark:text-emerald-400 flex items-center">
                <span className="w-2 h-2 bg-emerald-500 rounded-full mr-1.5 animate-pulse"></span>
                Online & Ready
              </p>
            </div>
          </div>

          <div className="flex space-x-1">
            <Button
              variant="ghost"
              size="sm"
              onClick={loadAllHistory}
              className="rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-300"
            >
              <History className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={clearAllHistory}
              className="rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-300"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={clearMessages}
              className="rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-300"
            >
              <Eraser className="h-4 w-4 mr-2" /> Clear
            </Button>
          </div>
        </div>

        {/* Error Banner */}
        {errorOccurred && (
          <div className="px-4 py-3 bg-red-50 dark:bg-red-900/20 border-b border-red-200 dark:border-red-800 flex justify-between items-center">
            <div className="flex items-start space-x-3">
              <div className="mt-0.5 p-1.5 bg-red-100 dark:bg-red-900/30 rounded-full">
                <X className="h-4 w-4 text-red-600 dark:text-red-400" />
              </div>
              <div>
                <p className="text-sm font-medium text-red-800 dark:text-red-200">
                  AI Response Error
                </p>
                <p className="text-xs text-red-600 dark:text-red-300">
                  {errorMessage.slice(0, 120)}
                  {errorMessage.length > 120 && '...'}
                </p>
              </div>
            </div>
            <button
              onClick={clearError}
              className="p-1.5 rounded-full hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors"
            >
              <X className="h-5 w-5 text-red-500 dark:text-red-400" />
            </button>
          </div>
        )}

        {/* Messages */}
        <div ref={scrollRef} className="flex-1 p-4 overflow-y-auto space-y-4 bg-gray-50/30 dark:bg-gray-800/20">
          {messages.map((m) => (
            <div
              key={m.id}
              className={cn(
                'flex max-w-3xl mx-auto w-full',
                m.role === 'user' ? 'ml-auto' : 'mr-auto'
              )}
            >
              <div className="w-8 flex-shrink-0">
                <div className={cn(
                  'h-8 w-8 flex items-center justify-center rounded-full flex-shrink-0',
                  m.role === 'user'
                    ? 'bg-gradient-to-br from-emerald-500 to-cyan-500 text-white ml-auto'
                    : 'bg-gradient-to-br from-gray-600 to-gray-700 text-white'
                )}>
                  {m.role === 'user' ? <User size={14} /> : <Bot size={14} />}
                </div>
              </div>
              <div className={cn(
                'ml-3 flex-1',
                m.role === 'user' ? 'text-right' : 'text-left'
              )}>
                <div className={cn(
                  'inline-block px-4 py-3 rounded-2xl text-sm shadow-sm max-w-full break-words',
                  m.role === 'user'
                    ? 'bg-gradient-to-br from-emerald-500 to-cyan-500 text-white rounded-br-md'
                    : 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-800 dark:text-gray-200 rounded-bl-md'
                )}>
                  {m.content}
                </div>
              </div>
            </div>
          ))}

          {plan && <PlanningSteps plan={plan} currentStepIndex={currentStepIndex} />}

          {isLoading && (
            <div className="flex max-w-3xl mx-auto w-full">
              <div className="w-8 flex-shrink-0">
                <div className="h-8 w-8 flex items-center justify-center rounded-full bg-gradient-to-br from-gray-600 to-gray-700 text-white flex-shrink-0">
                  <Bot size={14} />
                </div>
              </div>
              <div className="ml-3 flex-1">
                <div className="px-4 py-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-2xl rounded-bl-md text-gray-800 dark:text-gray-200 shadow-sm max-w-xs">
                  <div className="flex items-center space-x-2">
                    <Loader2 className="animate-spin h-4 w-4 text-emerald-600 dark:text-emerald-400" />
                    <span>Thinking...</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="p-4 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
          <form onSubmit={handleFormSubmit} className="max-w-3xl mx-auto">
            <div className="relative rounded-xl bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 shadow-sm focus-within:ring-2 focus-within:ring-emerald-500 focus-within:border-emerald-500">
              <textarea
                value={input}
                onChange={handleInputChange}
                rows={1}
                placeholder={isListening ? 'Listening…' : 'Message AI Assistant'}
                className="w-full px-4 py-3 bg-transparent border-0 focus:outline-none focus:ring-0 resize-none min-h-[48px] max-h-32"
              />
              <div className="absolute right-3 bottom-3 flex items-center space-x-2">
                <Button
                  type="button"
                  onClick={toggleVoice}
                  variant={isListening ? "danger" : "ghost"}
                  size="sm"
                  className="h-8 w-8 p-0 rounded-full"
                >
                  {isListening ? <MicOff className="h-4 w-4" /> : <Mic className="h-4 w-4" />}
                </Button>
                <Button
                  type="submit"
                  disabled={isLoading || !input.trim()}
                  className="h-8 w-8 p-0 rounded-full bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-600 hover:to-cyan-600"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
            <p className="text-xs text-center text-gray-500 dark:text-gray-400 mt-2">
              AI Assistant can make mistakes. Consider checking important information.
            </p>
          </form>
        </div>
      </div>
    </div>
  );
};
