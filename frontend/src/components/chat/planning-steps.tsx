'use client';

import React from 'react';
import { CheckCircle2, Circle, Loader2, XCircle } from 'lucide-react';
import { PlanStep } from '@/hooks/usePlanning';

interface PlanningStepsProps {
    plan: PlanStep[];
    currentStepIndex: number;
}

export const PlanningSteps: React.FC<PlanningStepsProps> = ({ plan, currentStepIndex }) => {
    if (plan.length === 0) return null;

    return (
        <div className="bg-gray-50 rounded-xl p-4 border border-gray-100 space-y-3">
            <h4 className="text-sm font-semibold text-gray-700 mb-2 flex items-center">
                <Loader2 className="h-4 w-4 mr-2 animate-spin text-emerald-600" />
                Executing Plan...
            </h4>
            <div className="space-y-4">
                {plan.map((step, index) => (
                    <div key={index} className="flex items-start">
                        <div className="mt-0.5 mr-3">
                            {step.status === 'completed' && <CheckCircle2 className="h-5 w-5 text-emerald-500" />}
                            {step.status === 'running' && <Loader2 className="h-5 w-5 text-emerald-600 animate-spin" />}
                            {step.status === 'pending' && <Circle className="h-5 w-5 text-gray-300" />}
                            {step.status === 'error' && <XCircle className="h-5 w-5 text-red-500" />}
                        </div>
                        <div className="flex-1">
                            <div className={`text-sm font-medium ${step.status === 'running' ? 'text-emerald-700' :
                                    step.status === 'completed' ? 'text-gray-900' : 'text-gray-500'
                                }`}>
                                {step.step}
                            </div>
                            <p className="text-xs text-gray-500 mt-0.5">{step.description}</p>
                            {step.error && (
                                <p className="text-xs text-red-500 mt-1 font-mono bg-red-50 p-1 rounded">{step.error}</p>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};
