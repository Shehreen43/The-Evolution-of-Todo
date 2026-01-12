# UI Components Specification

This document defines the UI components for the Full-Stack Todo Web Application, Phase II of "The Evolution of Todo" project.

## Overview

| Attribute | Value |
|-----------|-------|
| **Framework** | Next.js 16+ (App Router) |
| **Styling** | Tailwind CSS |
| **Status** | Draft |

---

## Design Principles

| Principle | Description |
|-----------|-------------|
| **Mobile-first** | Design for mobile first, then scale up |
| **Tailwind CSS** | All styling via Tailwind (no custom CSS) |
| **Accessible** | WCAG 2.1 AA compliance |
| **Consistent** | Unified spacing, typography, and colors |
| **States** | Loading and error states for all interactive components |
| **Optimistic UI** | Update UI immediately, revert on error |

---

## Component Hierarchy

```
App Layout
├── Navigation (Header)
├── Main Content Area
│   ├── Dashboard Page
│   │   ├── TaskList
│   │   │   └── TaskItem (multiple)
│   │   └── AddTaskForm
│   ├── Auth Pages
│   │   ├── SignUpForm
│   │   └── SignInForm
│   └── Protected Route Wrapper
└── Footer (optional)
```

---

## Core Components

### 1. TaskList Component

**Purpose:** Display list of tasks with filtering and sorting

**Location:** `app/components/TaskList.tsx`

**Props:**
```typescript
interface TaskListProps {
  tasks: Task[]
  onTaskUpdate: (taskId: number, updates: Partial<Task>) => void
  onTaskDelete: (taskId: number) => void
  onTaskToggle: (taskId: number) => void
  isLoading?: boolean
  error?: string | null
}
```

**Features:**
- Display all tasks in a list/grid
- Empty state when no tasks
- Filter controls (all/pending/completed)
- Sort controls (date/title)
- Loading skeleton while fetching
- Error message on fetch failure

**Layout:**
- Responsive grid/list layout
- Card-based design for each task
- Smooth animations for add/remove

**States:**
| State | UI |
|-------|-----|
| Loading | Show skeleton loaders |
| Empty | Show 'No tasks yet' message with illustration |
| Error | Show error message with retry button |
| Populated | Show task items |

**Tailwind Classes:**
```tsx
// Container
<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">

// Filter bar
<div className="flex gap-2 mb-4">

// Task card
<div className="bg-white rounded-lg shadow-md p-4">
```

---

### 2. TaskItem Component

**Purpose:** Display individual task with actions

**Location:** `app/components/TaskItem.tsx`

**Props:**
```typescript
interface TaskItemProps {
  task: Task
  onUpdate: (updates: Partial<Task>) => void
  onDelete: () => void
  onToggle: () => void
}
```

**Features:**
- Display title and description
- Checkbox for completion toggle
- Edit button (inline or modal)
- Delete button with confirmation
- Visual indication of completed state (strikethrough, opacity)
- Timestamps (created/updated)

**Layout:**
```tsx
// Card design
<div className={`
  bg-white rounded-lg shadow-md p-4 border
  ${task.completed ? 'border-gray-200 opacity-75' : 'border-l-4 border-l-blue-500'}
`}>
  {/* Checkbox on left */}
  <input type="checkbox" checked={completed} onChange={onToggle} />

  {/* Content in middle */}
  <div className="flex-1">
    <h3 className={`font-semibold ${completed ? 'line-through text-gray-500' : ''}`}>
      {task.title}
    </h3>
    {task.description && (
      <p className="text-gray-600 mt-1">{task.description}</p>
    )}
  </div>

  {/* Actions on right */}
  <div className="flex gap-2">
    <button onClick={onEdit} className="...">Edit</button>
    <button onClick={onDelete} className="...">Delete</button>
  </div>
</div>
```

**Interactions:**
- Click checkbox: toggle completion
- Click edit: open edit mode
- Click delete: show confirmation dialog
- Hover: show edit/delete buttons

**Responsive:**
- Mobile: stack vertically
- Desktop: horizontal layout

---

### 3. AddTaskForm Component

**Purpose:** Form to create new tasks

**Location:** `app/components/AddTaskForm.tsx`

**Props:**
```typescript
interface AddTaskFormProps {
  onSubmit: (task: CreateTaskData) => Promise<void>
}
```

**Features:**
- Title input (required, 1-200 chars)
- Description textarea (optional, max 1000 chars)
- Submit button (disabled during submission)
- Character count indicators
- Clear form after successful submission
- Error handling and display

**Validation:**
| Field | Rule | Error Message |
|-------|------|---------------|
| Title | Required | "Title is required" |
| Title | 1-200 chars | "Title must be 200 characters or less" |
| Description | 0-1000 chars | "Description must be 1000 characters or less" |

**Layout:**
```tsx
<form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6">
  <div className="mb-4">
    <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
      Title *
    </label>
    <input
      id="title"
      type="text"
      value={title}
      onChange={(e) => setTitle(e.target.value)}
      className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
      placeholder="What needs to be done?"
    />
    <p className="text-xs text-gray-500 mt-1">{title.length}/200 characters</p>
  </div>

  <div className="mb-4">
    <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
      Description (optional)
    </label>
    <textarea
      id="description"
      value={description}
      onChange={(e) => setDescription(e.target.value)}
      rows={3}
      className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
      placeholder="Add details..."
    />
    <p className="text-xs text-gray-500 mt-1">{description.length}/1000 characters</p>
  </div>

  <button
    type="submit"
    disabled={isSubmitting || !title.trim()}
    className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50"
  >
    {isSubmitting ? 'Adding...' : 'Add Task'}
  </button>
</form>
```

**States:**
| State | UI |
|-------|-----|
| Idle | Ready for input |
| Submitting | Show spinner, disable inputs |
| Success | Clear form, show success message |
| Error | Show error, keep form data |

---

### 4. EditTaskForm Component

**Purpose:** Edit existing task (modal or inline)

**Location:** `app/components/EditTaskForm.tsx`

**Props:**
```typescript
interface EditTaskFormProps {
  task: Task
  onSave: (updates: Partial<Task>) => Promise<void>
  onCancel: () => void
}
```

**Features:**
- Pre-populate with existing task data
- Same validation as AddTaskForm
- Save and Cancel buttons
- Loading state during save

**Layout:**
- Modal dialog (recommended) or inline replacement
- Same layout as AddTaskForm

```tsx
// Modal layout
<div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
  <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md">
    <h2 className="text-xl font-semibold mb-4">Edit Task</h2>
    {/* Form content same as AddTaskForm */}
  </div>
</div>
```

---

### 5. SignUpForm Component

**Purpose:** User registration form

**Location:** `app/(auth)/signup/page.tsx`

**Fields:**
| Field | Type | Validation |
|-------|------|------------|
| Name | text | Required, min 2 chars |
| Email | email | Required, valid format |
| Password | password | Required, min 8 chars |
| Confirm Password | password | Must match password |

**Features:**
- Client-side validation
- Show/hide password toggle
- Password strength indicator
- Submit button with loading state
- Error messages for validation failures
- Link to sign-in page
- Redirect to dashboard after successful signup

**Layout:**
```tsx
<form onSubmit={handleSubmit} className="space-y-4">
  <div>
    <label htmlFor="name" className="block text-sm font-medium text-gray-700">
      Name
    </label>
    <input
      id="name"
      type="text"
      value={name}
      onChange={(e) => setName(e.target.value)}
      className="mt-1 w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
    />
    {errors.name && <p className="text-red-500 text-sm mt-1">{errors.name}</p>}
  </div>

  <div>
    <label htmlFor="email" className="block text-sm font-medium text-gray-700">
      Email
    </label>
    <input
      id="email"
      type="email"
      value={email}
      onChange={(e) => setEmail(e.target.value)}
      className="mt-1 w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
    />
    {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email}</p>}
  </div>

  <div>
    <label htmlFor="password" className="block text-sm font-medium text-gray-700">
      Password
    </label>
    <div className="relative">
      <input
        id="password"
        type={showPassword ? 'text' : 'password'}
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="mt-1 w-full border border-gray-300 rounded-lg px-4 py-2 pr-10 focus:ring-2 focus:ring-blue-500"
      />
      <button
        type="button"
        onClick={() => setShowPassword(!showPassword)}
        className="absolute right-3 top-3 text-gray-500"
      >
        {showPassword ? 'Hide' : 'Show'}
      </button>
    </div>
    {errors.password && <p className="text-red-500 text-sm mt-1">{errors.password}</p>}
  </div>

  <button
    type="submit"
    disabled={isSubmitting}
    className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50"
  >
    {isSubmitting ? 'Creating account...' : 'Create Account'}
  </button>

  <p className="text-center text-sm text-gray-600">
    Already have an account?{' '}
    <Link href="/signin" className="text-blue-600 hover:underline">
      Sign in
    </Link>
  </p>
</form>
```

---

### 6. SignInForm Component

**Purpose:** User login form

**Location:** `app/(auth)/signin/page.tsx`

**Fields:**
| Field | Type | Validation |
|-------|------|------------|
| Email | email | Required, valid format |
| Password | password | Required |

**Features:**
- Client-side validation
- Show/hide password toggle
- Remember me checkbox (optional)
- Submit button with loading state
- Error messages for invalid credentials
- Link to sign-up page
- Forgot password link (optional)
- Redirect to dashboard after successful login

---

### 7. Navigation Component

**Purpose:** Main app navigation/header

**Location:** `app/components/Navigation.tsx`

**Features:**
- App logo/title
- User display (when logged in)
  - Show user name
  - Avatar (optional)
  - Sign out button
- Responsive: collapse to hamburger on mobile

**Conditional Display:**
```tsx
// When logged in
<nav className="bg-white shadow-md">
  <div className="max-w-7xl mx-auto px-4">
    <div className="flex justify-between h-16">
      <div className="flex items-center">
        <Link href="/dashboard" className="text-xl font-bold text-blue-600">
          Todo App
        </Link>
      </div>

      <div className="flex items-center gap-4">
        <span className="text-gray-700">{user.name}</span>
        <button
          onClick={handleSignOut}
          className="text-gray-600 hover:text-gray-900"
        >
          Sign Out
        </button>
      </div>
    </div>
  </div>
</nav>

// When logged out
<nav className="bg-white shadow-md">
  <div className="max-w-7xl mx-auto px-4">
    <div className="flex justify-between h-16 items-center">
      <Link href="/" className="text-xl font-bold text-blue-600">
        Todo App
      </Link>

      <div className="flex gap-4">
        <Link href="/signin" className="text-gray-600 hover:text-gray-900">
          Sign In
        </Link>
        <Link
          href="/signup"
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          Sign Up
        </Link>
      </div>
    </div>
  </div>
</nav>
```

---

### 8. ProtectedRoute Component

**Purpose:** Wrapper that ensures user is authenticated

**Location:** `app/components/ProtectedRoute.tsx`

**Features:**
- Check authentication status
- Redirect to `/signin` if not authenticated
- Show loading while checking auth status
- Preserve intended destination (return URL)

```tsx
export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { data: session, isLoading } = useSession()

  if (isLoading) {
    return <LoadingSpinner />
  }

  if (!session) {
    // Save current URL for redirect after login
    return <Navigate to="/signin" state={{ from: window.location.href }} replace />
  }

  return <>{children}</>
}
```

---

### 9. ConfirmDialog Component

**Purpose:** Reusable confirmation modal

**Location:** `app/components/ConfirmDialog.tsx`

**Props:**
```typescript
interface ConfirmDialogProps {
  isOpen: boolean
  title: string
  message: string
  onConfirm: () => void
  onCancel: () => void
  confirmText?: string
  cancelText?: string
  variant?: 'danger' | 'warning' | 'info'
}
```

**Layout:**
```tsx
{isOpen && (
  <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-sm">
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-gray-600 mb-6">{message}</p>

      <div className="flex gap-3 justify-end">
        <button
          onClick={onCancel}
          className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200"
        >
          {cancelText || 'Cancel'}
        </button>
        <button
          onClick={onConfirm}
          className={`px-4 py-2 text-white rounded-lg ${
            variant === 'danger' ? 'bg-red-600 hover:bg-red-700' : 'bg-blue-600 hover:bg-blue-700'
          }`}
        >
          {confirmText || 'Confirm'}
        </button>
      </div>
    </div>
  </div>
)}
```

**Usage:** Used for delete task confirmation

---

### 10. LoadingSpinner Component

**Purpose:** Reusable loading indicator

**Location:** `app/components/LoadingSpinner.tsx`

**Variants:**
| Variant | Tailwind Classes | Usage |
|---------|------------------|-------|
| Full page | `flex items-center justify-center h-screen` | During page load |
| Inline | `inline-block mr-2` | During async actions |
| Button | `animate-spin mr-2` | During form submission |

**Implementation:**
```tsx
export function LoadingSpinner({ size = 'md', className = '' }: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
  }

  return (
    <svg
      className={`animate-spin ${sizeClasses[size]} ${className}`}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
  )
}
```

---

## Shared UI Patterns

### Buttons

| Variant | Tailwind Classes | Usage |
|---------|------------------|-------|
| Primary | `bg-blue-600 hover:bg-blue-700 text-white` | Main actions (submit, save) |
| Secondary | `bg-gray-600 hover:bg-gray-700 text-white` | Cancel, back |
| Danger | `bg-red-600 hover:bg-red-700 text-white` | Delete, confirm delete |
| Disabled | `opacity-50 cursor-not-allowed` | When action unavailable |

### Inputs

| State | Tailwind Classes |
|-------|------------------|
| Default | `border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500` |
| Error | `border border-red-500 focus:ring-2 focus:ring-red-500` |
| Disabled | `bg-gray-100 cursor-not-allowed` |

### Cards

| Property | Tailwind Classes |
|----------|------------------|
| Container | `bg-white rounded-lg shadow-md` |
| Padding | `p-4` or `p-6` |
| Border | `border border-gray-200` |
| Hover | `hover:shadow-lg transition-shadow` |

### Colors

| Purpose | Tailwind Classes |
|---------|------------------|
| Primary | `text-blue-600`, `bg-blue-600` |
| Success | `text-green-600`, `bg-green-600` |
| Error | `text-red-600`, `bg-red-600` |
| Warning | `text-yellow-600`, `bg-yellow-600` |
| Neutral | `text-gray-600`, `bg-gray-100` |

### Spacing

| Purpose | Tailwind Classes |
|---------|------------------|
| Container | `max-w-7xl mx-auto px-4` |
| Between items | `gap-4` or `gap-6` |
| Inside card | `p-4` or `p-6` |
| Between fields | `mb-4` |

### Typography

| Element | Tailwind Classes |
|---------|------------------|
| Page title | `text-2xl font-bold text-gray-900` |
| Section title | `text-xl font-semibold text-gray-800` |
| Card title | `text-lg font-medium text-gray-900` |
| Body text | `text-gray-600` |
| Caption | `text-sm text-gray-500` |

---

## Accessibility (WCAG 2.1 AA)

| Requirement | Implementation |
|-------------|----------------|
| Color contrast | Minimum 4.5:1 for text |
| Focus indicators | Visible outline on keyboard focus |
| ARIA labels | For icons and non-text inputs |
| Form labels | All inputs have associated labels |
| Keyboard navigation | All interactions via keyboard |
| Screen reader support | Semantic HTML elements |

---

## Responsive Breakpoints

| Breakpoint | Tailwind Prefix | Width |
|------------|-----------------|-------|
| Mobile | Default | < 640px |
| Tablet | `md:` | 640px - 1023px |
| Desktop | `lg:` | 1024px - 1279px |
| Large | `xl:` | >= 1280px |

---

## Related Documents

| Document | Path | Purpose |
|----------|------|---------|
| Architecture | `architecture.md` | System architecture |
| API Spec | `api/rest-endpoints.md` | API endpoints |
| Task CRUD | `features/task-crud.md` | Task operations |
| Authentication | `features/authentication.md` | Auth flow |

---

## Component Architecture

### Atomic Design Pattern
Components will follow the atomic design methodology:

```
Atoms (Primitive Elements)
├── Button, Input, Icon, Typography
├── Label, Checkbox, Radio
├── Image, Link

Molecules (Compound Elements)
├── InputGroup, ButtonGroup
├── TaskCard, Modal, Toast
├── FormField, SearchBox

Organisms (Complex Components)
├── Header, Sidebar, Navigation
├── TaskList, TaskForm
├── PageLayout

Templates (Page Structures)
├── Dashboard Template
├── Auth Page Template
├── Settings Template

Pages (Specific Views)
├── Dashboard Page
├── Sign In Page
├── Settings Page
```

### Technology Stack
| Aspect | Technology |
|--------|------------|
| **Framework** | React 18+ with TypeScript |
| **Styling** | Tailwind CSS v3+ |
| **Component Type** | React Server Components (default), Client Components (when needed) |
| **Type Safety** | Strict TypeScript with PropTypes |

### Component Structure
```
app/
├── components/
│   ├── atoms/
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   └── Icon.tsx
│   ├── molecules/
│   │   ├── TaskCard.tsx
│   │   ├── Modal.tsx
│   │   ├── Toast.tsx
│   │   └── ConfirmDialog.tsx
│   ├── organisms/
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   ├── TaskList.tsx
│   │   ├── TaskForm.tsx
│   │   └── PageLayout.tsx
│   └── ui/
│       ├── SignInForm.tsx
│       └── SignUpForm.tsx
```

---

## Core Components

### TaskCard (Molecule)

**Purpose:** Display individual task in list

**Location:** `app/components/molecules/TaskCard.tsx`

**Props:**
```typescript
interface TaskCardProps {
  task: Task
  onToggle: (id: number) => void
  onEdit: (id: number) => void
  onDelete: (id: number) => void
}
```

**Features:**
- Checkbox for completion toggle
- Strike-through text when completed
- Edit icon button
- Delete icon button with confirmation
- Timestamp display (relative: "2 hours ago")

**Layout:**
```tsx
<div className={`
  bg-white rounded-lg border shadow-sm p-4
  hover:shadow-md transition-shadow duration-200
  ${task.completed ? 'opacity-75' : ''}
`}>
  <div className="flex items-start gap-3">
    <input
      type="checkbox"
      checked={task.completed}
      onChange={() => onToggle(task.id)}
      className="mt-1 h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
    />

    <div className="flex-1 min-w-0">
      <h3 className={`
        font-medium truncate
        ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}
      `}>
        {task.title}
      </h3>

      {task.description && (
        <p className="text-gray-600 text-sm mt-1 truncate">
          {task.description}
        </p>
      )}

      <p className="text-gray-400 text-xs mt-2">
        {formatRelativeTime(task.createdAt)}
      </p>
    </div>

    <div className="flex gap-2">
      <button
        onClick={() => onEdit(task.id)}
        className="text-gray-400 hover:text-blue-600"
        aria-label="Edit task"
      >
        <EditIcon />
      </button>
      <button
        onClick={() => onDelete(task.id)}
        className="text-gray-400 hover:text-red-600"
        aria-label="Delete task"
      >
        <DeleteIcon />
      </button>
    </div>
  </div>
</div>
```

**States:**
| State | UI |
|-------|-----|
| Pending | Normal appearance with blue accent |
| Completed | Strike-through title, reduced opacity |
| Hover | Subtle shadow enhancement |
| Loading | Skeleton loader state |

---

### TaskList (Organism)

**Purpose:** Container for multiple TaskCard components

**Location:** `app/components/organisms/TaskList.tsx`

**Props:**
```typescript
interface TaskListProps {
  tasks: Task[]
  loading: boolean
  emptyMessage?: string
  onToggle: (id: number) => void
  onEdit: (id: number) => void
  onDelete: (id: number) => void
}
```

**Features:**
- Grid/list view toggle
- Loading skeleton
- Empty state illustration
- Virtualization for large lists (>100 items)

**Layout:**
```tsx
<div className="space-y-4">
  {/* Controls */}
  <div className="flex justify-between items-center">
    <h2 className="text-lg font-semibold text-gray-900">Tasks</h2>
    <div className="flex gap-2">
      <ViewToggle />
    </div>
  </div>

  {/* Loading state */}
  {loading && (
    <div className="grid gap-4">
      {[...Array(5)].map((_, i) => (
        <TaskCardSkeleton key={i} />
      ))}
    </div>
  )}

  {/* Empty state */}
  {!loading && tasks.length === 0 && (
    <EmptyState message={emptyMessage || "No tasks yet"} />
  )}

  {/* Task cards */}
  {!loading && tasks.length > 0 && (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {tasks.map(task => (
        <TaskCard
          key={task.id}
          task={task}
          onToggle={onToggle}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </div>
  )}
</div>
```

---

### TaskForm (Organism)

**Purpose:** Create/edit task form

**Location:** `app/components/organisms/TaskForm.tsx`

**Props:**
```typescript
interface TaskFormProps {
  initialData?: Task
  onSubmit: (data: TaskInput) => void
  onCancel: () => void
}
```

**Fields:**
- Title input (required, character counter)
- Description textarea (optional, expandable)
- Submit button (disabled during loading)
- Cancel button

**Validation:**
- Real-time validation
- Error messages below fields
- Submit disabled if invalid

**Layout:**
```tsx
<form onSubmit={handleSubmit} className="space-y-4">
  <div>
    <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
      Title *
    </label>
    <input
      id="title"
      type="text"
      value={formData.title}
      onChange={(e) => setFormData({...formData, title: e.target.value})}
      className={`
        w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500
        ${errors.title ? 'border-red-500' : 'border-gray-300'}
      `}
      placeholder="Enter task title"
      maxLength={100}
    />
    {errors.title && <p className="text-red-500 text-xs mt-1">{errors.title}</p>}
    <p className="text-xs text-gray-500 mt-1">{formData.title.length}/100</p>
  </div>

  <div>
    <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
      Description
    </label>
    <textarea
      id="description"
      value={formData.description}
      onChange={(e) => setFormData({...formData, description: e.target.value})}
      rows={3}
      className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
      placeholder="Enter task description (optional)"
      maxLength={500}
    />
    <p className="text-xs text-gray-500 mt-1">{formData.description.length}/500</p>
  </div>

  <div className="flex gap-3 pt-2">
    <button
      type="submit"
      disabled={isSubmitting || !isValid}
      className="
        flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg
        hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed
      "
    >
      {isSubmitting ? 'Saving...' : 'Save Task'}
    </button>
    <button
      type="button"
      onClick={onCancel}
      className="px-4 py-2 text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50"
    >
      Cancel
    </button>
  </div>
</form>
```

---

### Button (Atom)

**Purpose:** Reusable button component with variants

**Location:** `app/components/atoms/Button.tsx`

**Props:**
```typescript
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  children: React.ReactNode
}
```

**Variants:**
- Primary: Main actions
- Secondary: Alternative actions
- Danger: Destructive actions
- Ghost: Minimal styling for subtle actions

**Sizes:**
- sm: Small buttons (icon buttons)
- md: Medium/default size
- lg: Large buttons

**States:**
- Default: Normal appearance
- Hover: Enhanced appearance
- Active: Pressed state
- Disabled: Inactive state
- Loading: Spinner with disabled appearance

**Layout:**
```tsx
<button
  {...props}
  disabled={disabled || loading}
  className={`
    inline-flex items-center justify-center rounded-lg font-medium
    transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2
    ${variantStyles[variant]}
    ${sizeStyles[size]}
    ${disabled || loading ? 'opacity-50 cursor-not-allowed' : ''}
    ${className}
  `}
>
  {loading && <Spinner className="mr-2 h-4 w-4" />}
  {children}
</button>
```

---

### Input (Atom)

**Purpose:** Reusable input component with various types

**Location:** `app/components/atoms/Input.tsx`

**Props:**
```typescript
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  type?: 'text' | 'email' | 'password' | 'textarea'
  error?: string
  helperText?: string
  label?: string
}
```

**Types:**
- text: Standard text input
- email: Email validation
- password: Password masking
- textarea: Multi-line input

**Features:**
- Error state styling
- Helper text display
- Label support

**Layout:**
```tsx
<div className="space-y-1">
  {label && (
    <label className="block text-sm font-medium text-gray-700">
      {label}
    </label>
  )}
  <input
    {...props}
    className={`
      w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500
      ${error ? 'border-red-500' : 'border-gray-300'}
      ${className}
    `}
  />
  {helperText && <p className="text-xs text-gray-500">{helperText}</p>}
  {error && <p className="text-xs text-red-500">{error}</p>}
</div>
```

---

### Modal (Molecule)

**Purpose:** Overlay dialogs for important interactions

**Location:** `app/components/molecules/Modal.tsx`

**Props:**
```typescript
interface ModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  children: React.ReactNode
  size?: 'sm' | 'md' | 'lg'
}
```

**Features:**
- Backdrop click to close
- ESC key support
- Focus trap
- Responsive sizing

**Layout:**
```tsx
{isOpen && (
  <div
    className="fixed inset-0 z-50 overflow-y-auto"
    onClick={onClose}
  >
    <div className="flex min-h-screen items-center justify-center p-4">
      <div
        className="fixed inset-0 bg-black bg-opacity-50"
        aria-hidden="true"
      />

      <div
        className={`
          relative bg-white rounded-lg shadow-xl overflow-hidden
          max-w-${size} w-full mx-auto
        `}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between p-6 border-b">
          <h3 className="text-lg font-medium text-gray-900">
            {title}
          </h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
          >
            <CloseIcon />
          </button>
        </div>

        <div className="p-6">
          {children}
        </div>
      </div>
    </div>
  </div>
)}
```

---

### Toast (Molecule)

**Purpose:** Notification messages for user feedback

**Location:** `app/components/molecules/Toast.tsx`

**Props:**
```typescript
interface ToastProps {
  message: string
  variant?: 'success' | 'error' | 'warning' | 'info'
  onClose: () => void
}
```

**Variants:**
- Success: Positive feedback
- Error: Error notifications
- Warning: Caution messages
- Info: Informational messages

**Features:**
- Auto-dismiss after 5 seconds
- Close button
- Positioning at top-right of screen

**Layout:**
```tsx
<div
  className={`
    fixed top-4 right-4 z-50 max-w-sm p-4 rounded-lg shadow-lg
    ${variantStyles[variant]}
  `}
>
  <div className="flex items-start gap-3">
    <div className="flex-shrink-0">
      <Icon variant={variant} />
    </div>
    <div className="flex-1">
      <p className="text-sm font-medium text-white">
        {message}
      </p>
    </div>
    <button
      onClick={onClose}
      className="text-white hover:text-gray-200"
    >
      <CloseIcon />
    </button>
  </div>
</div>
```

---

## Layout Components

### Header

**Purpose:** Main application header with navigation and user controls

**Location:** `app/components/organisms/Header.tsx`

**Features:**
- Logo display
- Navigation links
- User menu (avatar, dropdown)
- Sign out button

**Layout:**
```tsx
<header className="sticky top-0 z-10 bg-white border-b border-gray-200">
  <div className="mx-auto px-4 sm:px-6 lg:px-8">
    <div className="flex items-center justify-between h-16">
      {/* Logo */}
      <div className="flex items-center">
        <Link href="/dashboard" className="flex-shrink-0">
          <span className="text-xl font-bold text-blue-600">Todo App</span>
        </Link>

        {/* Navigation links */}
        <nav className="ml-10 hidden md:flex space-x-8">
          <Link href="/dashboard" className="text-gray-900 hover:text-blue-600">
            Dashboard
          </Link>
          <Link href="/settings" className="text-gray-500 hover:text-blue-600">
            Settings
          </Link>
        </nav>
      </div>

      {/* User menu */}
      <div className="flex items-center">
        <div className="relative ml-3">
          <div className="flex items-center space-x-3">
            <div className="text-sm">
              <p className="font-medium text-gray-900">{user.name}</p>
            </div>
            <button className="flex text-sm rounded-full focus:outline-none">
              <Avatar user={user} />
            </button>

            <Menu>
              <Menu.Item>
                <button className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                  Profile
                </button>
              </Menu.Item>
              <Menu.Item>
                <button
                  onClick={signOut}
                  className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  Sign out
                </button>
              </Menu.Item>
            </Menu>
          </div>
        </div>
      </div>
    </div>
  </div>
</header>
```

---

### Sidebar

**Purpose:** Navigation sidebar with collapsible behavior

**Location:** `app/components/organisms/Sidebar.tsx`

**Features:**
- Navigation items
- Active state indication
- Collapsible on mobile

**Layout:**
```tsx
<div className="hidden md:block">
  <div className="flex flex-col h-full">
    <nav className="flex-1 px-2 py-4 space-y-1">
      <Link
        href="/dashboard"
        className="bg-blue-100 text-blue-700 group flex items-center px-2 py-2 text-sm font-medium rounded-md"
      >
        <DashboardIcon className="text-blue-500 mr-3" />
        Dashboard
      </Link>
      <Link
        href="/tasks"
        className="text-gray-600 hover:bg-gray-50 hover:text-gray-900 group flex items-center px-2 py-2 text-sm font-medium rounded-md"
      >
        <TaskIcon className="text-gray-400 mr-3" />
        Tasks
      </Link>
    </nav>
  </div>
</div>

{/* Mobile menu */}
<div className="md:hidden">
  <MobileMenu />
</div>
```

---

### PageLayout

**Purpose:** Main layout wrapper for pages

**Location:** `app/components/organisms/PageLayout.tsx`

**Features:**
- Header + Sidebar + Main content area
- Responsive breakpoints

**Layout:**
```tsx
export function PageLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />

      <div className="flex">
        <Sidebar />

        <main className="flex-1 pb-8">
          <div className="mx-auto px-4 sm:px-6 lg:px-8 py-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}
```

---

## Authentication Components

### SignInForm

**Purpose:** User authentication form

**Location:** `app/components/ui/SignInForm.tsx`

**Features:**
- Email input
- Password input (with visibility toggle)
- Remember me checkbox
- Submit button
- Forgot password link
- Sign up link

**Layout:**
```tsx
<form onSubmit={handleSubmit} className="space-y-6">
  <div>
    <label htmlFor="email" className="block text-sm font-medium text-gray-700">
      Email address
    </label>
    <input
      id="email"
      name="email"
      type="email"
      required
      value={email}
      onChange={(e) => setEmail(e.target.value)}
      className="mt-1 block w-full border border-gray-300 rounded-md px-4 py-2 shadow-sm focus:ring-blue-500 focus:border-blue-500"
    />
  </div>

  <div>
    <label htmlFor="password" className="block text-sm font-medium text-gray-700">
      Password
    </label>
    <div className="mt-1 relative">
      <input
        id="password"
        name="password"
        type={showPassword ? "text" : "password"}
        required
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="block w-full border border-gray-300 rounded-md px-4 py-2 pr-10 shadow-sm focus:ring-blue-500 focus:border-blue-500"
      />
      <button
        type="button"
        className="absolute inset-y-0 right-0 pr-3 flex items-center"
        onClick={() => setShowPassword(!showPassword)}
      >
        {showPassword ? <EyeOffIcon /> : <EyeIcon />}
      </button>
    </div>
  </div>

  <div className="flex items-center justify-between">
    <div className="flex items-center">
      <input
        id="remember-me"
        name="remember-me"
        type="checkbox"
        className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
      />
      <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900">
        Remember me
      </label>
    </div>

    <div className="text-sm">
      <a href="/forgot-password" className="font-medium text-blue-600 hover:text-blue-500">
        Forgot your password?
      </a>
    </div>
  </div>

  <div>
    <button
      type="submit"
      disabled={isSubmitting}
      className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
    >
      {isSubmitting ? 'Signing in...' : 'Sign in'}
    </button>
  </div>
</form>

<div className="mt-6 text-center text-sm">
  <p>
    Don't have an account?{' '}
    <Link to="/signup" className="font-medium text-blue-600 hover:text-blue-500">
      Sign up
    </Link>
  </p>
</div>
```

---

## Version Information

| Item | Value |
|------|-------|
| UI Specification | 1.0.0 |
| Status | Draft |
| Last Updated | 2026-01-07 |
