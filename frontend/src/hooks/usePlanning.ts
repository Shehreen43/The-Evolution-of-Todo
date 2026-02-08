'use client';

import { useState, useCallback } from 'react';

export interface PlanStep {
    step: string;
    description: string;
    tool: string;
    arguments: Record<string, any>;
    status: 'pending' | 'running' | 'completed' | 'error';
    error?: string;
}

export function usePlanning() {
    const [plan, setPlan] = useState<PlanStep[]>([]);
    const [currentStepIndex, setCurrentStepIndex] = useState(-1);
    const [isExecuting, setIsExecuting] = useState(false);

    const updateStepStatus = useCallback((index: number, status: PlanStep['status'], error?: string) => {
        setPlan(prev => prev.map((step, i) =>
            i === index ? { ...step, status, error } : step
        ));
    }, []);

    const resetPlan = useCallback(() => {
        setPlan([]);
        setCurrentStepIndex(-1);
        setIsExecuting(false);
    }, []);

    return {
        plan,
        setPlan,
        currentStepIndex,
        setCurrentStepIndex,
        isExecuting,
        setIsExecuting,
        updateStepStatus,
        resetPlan
    };
}
