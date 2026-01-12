# The Evolution of Todo - Frontend

This is the Next.js frontend for the Phase II Todo application with authentication.

## Tech Stack
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- React

## Features
- User authentication with JWT tokens
- Task management (Create, Read, Update, Delete)
- Task completion toggling
- Priority levels (low, medium, high)
- Responsive design with dark mode support

## Environment Variables
- `NEXT_PUBLIC_API_URL` - Backend API base URL (defaults to http://localhost:8000)

## Installation
```bash
npm install
```

## Running the Application
```bash
npm run dev
```

## Key Components
- `src/components/TodoList.tsx` - Main todo functionality
- `src/context/AuthContext.tsx` - Authentication management
- `src/lib/api.ts` - API client with JWT handling
- `src/app/page.tsx` - Main application page
