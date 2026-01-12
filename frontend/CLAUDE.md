# Frontend Guidelines

## Stack
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- React Client Components

## Folder Structure
```
frontend/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── layout.tsx       # Root layout with AuthProvider
│   │   ├── page.tsx         # Main todo page
│   │   └── globals.css      # Global styles
│   ├── components/          # Reusable UI components
│   │   └── TodoList.tsx     # Main todo functionality component
│   ├── context/             # React context providers
│   │   └── AuthContext.tsx  # Authentication context
│   ├── lib/                 # Utilities and API client
│   │   └── api.ts           # API client with JWT handling
│   └── types/               # Type definitions (if needed)
```

## Authentication Flow
- JWT tokens issued by backend (Better Auth or custom implementation)
- Token stored in localStorage
- Token attached to API requests as `Authorization: Bearer <token>`
- User ID extracted from JWT claims

## API Integration
- All backend calls use the api client: `@/lib/api`
- API endpoints follow the pattern: `/api/{user_id}/{resource}`
- JWT token automatically attached to requests
- Error handling with proper user feedback

## Component Structure
- Use Client Components (`'use client'`) when needed for interactivity
- Server Components by default for static content
- Reusable components in `/components` directory
- Shared context providers in `/context` directory

## Styling
- Use Tailwind CSS utility classes
- Follow consistent color palette
- Responsive design with mobile-first approach
- Dark mode support using `dark:` variants

## Environment Variables
- `NEXT_PUBLIC_API_URL` - Backend API base URL (defaults to http://localhost:8000)

## Key Features Implemented
- Task CRUD operations (Create, Read, Update, Delete)
- Toggle task completion status
- Priority levels (low, medium, high)
- User authentication and token management
- Responsive UI with Tailwind CSS
- Error handling and loading states