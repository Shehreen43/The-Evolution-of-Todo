# Phase III: Todo AI Chatbot - Overview

## 1.1 PROJECT SUMMARY

### Phase III Objectives and Scope
Phase III of the Todo AI Chatbot project aims to transform the existing basic Todo CRUD application into an intelligent, natural language-driven interface. The primary objective is to enable users to manage their todos through conversational interactions using both text and voice commands, while maintaining cost efficiency through free and low-cost resources.

The scope includes:
- Implementation of an AI-powered chatbot interface for todo management
- Support for both text-based and voice-based interactions
- Integration with existing Phase II application features (authentication, database, CRUD operations)
- Implementation of MCP (Model Context Protocol) server architecture for enhanced AI tool integration
- Optimization for free-tier usage and cost-effective operation

### Key Differentiators
- **Free-tier Optimization**: Designed to operate primarily on free-tier resources and services, making the solution accessible to a broader audience
- **Voice Support**: Native support for speech-to-text and text-to-speech capabilities, enabling hands-free todo management
- **Intelligent Processing**: Natural language understanding for complex todo operations (scheduling, prioritization, categorization)
- **MCP Protocol Integration**: Implementation of Model Context Protocol for enhanced AI tool interoperability

### Integration with Existing Phase II Application
The AI chatbot will seamlessly integrate with the existing Phase II infrastructure, leveraging:
- The existing Neon PostgreSQL database for data persistence
- Better Auth for user authentication and session management
- The FastAPI backend for API operations
- All existing todo CRUD functionality while adding conversational interfaces

## 1.2 TECHNOLOGY STACK

| Component | Technology | Purpose | Cost |
|-----------|-----------|---------|------|
| Frontend UI | OpenAI ChatKit | Chat interface | Free |
| Voice Input | Web Speech API (STT) | Speech-to-Text | Free (Browser) |
| Voice Output | Web Speech API (TTS) | Text-to-Speech | Free (Browser) |
| Backend | Python FastAPI | API Server | Free (Self-hosted) |
| AI Client | OpenAI Python SDK | LLM Integration | Free (SDK) |
| AI Provider | OpenRouter | LLM Gateway | Free/Low-cost Models |
| Recommended Models | Llama 3.1 8B, Gemini Flash 1.5 | Free-tier options | Free |
| MCP Server | Official MCP SDK (Python) | Tool Protocol | Free |
| ORM | SQLModel | Database Models | Free |
| Database | Neon Serverless PostgreSQL | Data Persistence | Free (Serverless) |