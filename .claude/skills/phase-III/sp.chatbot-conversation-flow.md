---
name: sp.chatbot-conversation-flow
description: Design and implement intelligent conversation flows for the AI todo chatbot. Manages dialogue state, handles follow-up questions, and provides contextual responses based on conversation history.
---

# Chatbot Conversation Flow for Todo Application

Design and implement intelligent conversation flows for the AI todo chatbot following Phase III specifications.

## Prerequisites

Verify:
- Backend API is operational (Phase II)
- AI model integration is established (Phase III)
- MCP server infrastructure is available (Phase III)
- Database schema supports conversation tracking (Phase III)

## Implementation Workflow

### 1. Design Conversation State Management

Create state management system:
- Active conversation context tracking
- Task reference resolution (pronouns, "that task", etc.)
- Intent persistence across multiple turns
- Session timeout and cleanup mechanisms

### 2. Implement Dialogue Act Recognition

Build capability to recognize:
- Task creation requests ("add a task to buy groceries")
- Task modification requests ("change the due date")
- Information retrieval ("show me my tasks", "what's left?")
- Task completion ("mark that as done", "complete task 3")
- Confirmation and clarification requests
- Conversation termination

### 3. Build Context Resolution Engine

Implement context resolution:
- Pronoun resolution ("it", "that", "the task")
- Implicit task references ("update it", "delete that")
- Temporal context ("yesterday", "next week", "by Friday")
- Relative positioning ("first task", "last one", "second item")

### 4. Create Conversation Patterns

Design common conversation patterns:
- Task creation with guided information gathering
- Multi-step task modification workflows
- Contextual help and suggestions
- Error recovery and clarification dialogs
- Confirmation chains for destructive operations

### 5. Implement Memory Management

Add conversation memory features:
- Short-term context retention (current session)
- Long-term preference learning
- Task relationship mapping
- User interaction pattern recognition

### 6. Add Personalization Features

Include personalization elements:
- User preference adaptation
- Conversation style customization
- Common task shortcut recognition
- Proactive suggestions based on history

## File Structure

### app/conversations/state_manager.py
Conversation state and context management system.

### app/conversations/dialogue_analyzer.py
Dialogue act recognition and intent classification.

### app/conversations/context_resolver.py
Context and reference resolution engine.

### app/conversations/flow_controller.py
Main conversation flow control logic.

### app/conversations/patterns.py
Predefined conversation patterns and templates.

### app/conversations/memory.py
Short-term and long-term memory management.

### app/conversations/personalization.py
User preference and style adaptation.

### app/conversations/utils.py
Utility functions for conversation processing.

## Configuration Requirements

### Environment Variables
- CONVERSATION_TIMEOUT_MINUTES
- MAX_CONTEXT_HISTORY_LENGTH
- PERSONALIZATION_ENABLED
- CONTEXT_RESOLUTION_THRESHOLD

### Flow Configuration
- Default conversation patterns
- Timeout settings for different contexts
- Memory retention policies
- Personalization sensitivity levels

## Quality Assurance

### Testing Requirements
- Unit tests for context resolution algorithms
- Integration tests for conversation state management
- End-to-end tests for complex multi-turn conversations
- Edge case testing for ambiguous references

### Performance Requirements
- Context resolution under 100ms
- Support for concurrent conversations
- Memory-efficient state management
- Scalable conversation history storage

## Guardrails

### Do
- Implement robust pronoun and reference resolution
- Provide clear feedback for ambiguous requests
- Maintain conversation context appropriately
- Respect user privacy in memory management
- Handle edge cases gracefully

### Do Not
- Persist sensitive information unnecessarily
- Make assumptions without confirmation
- Lose conversation context unexpectedly
- Allow infinite conversation loops

### Defer
- Advanced personality modeling
- Emotional state detection
- Complex multi-user conversations
- Cross-session context persistence beyond preferences

## Triggers

Use this skill when:
- User requests conversation flow implementation for todo chatbot
- Starting Phase III dialogue management development
- Need to improve contextual understanding and responses
- Setting up intelligent follow-up question handling
- Designing personalized conversation experiences