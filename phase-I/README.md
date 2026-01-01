<div align="center">

  <!-- Logo -->
  <img src="https://img.shields.io/badge/python-3.13+-blue.svg" alt="Python 3.13+" />
  <img src="https://img.shields.io/badge/platform-windows%20%7C%20Linux-lightgrey.svg" alt="Platform" />
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License" />
  <img src="https://img.shields.io/badge/version-1.0.0-orange.svg" alt="Version" />

</div>

# 🎯 Phase I - Todo Console App

<div align="center">
  <b>A beautiful, interactive command-line todo application with rich emoji support and in-memory storage</b>
</div>

---

## ✨ Highlights

- 🎨 **Beautiful ASCII Art Banner** - Large H1-style welcome message
- ✨ **Rich Emoji Indicators** - Visual feedback for all operations
- 🎨 **Color-Coded Output** - Easy-to-read status messages
- ⚡ **Interactive Mode** - User-friendly guided prompts
- 📋 **Formatted Tables** - Clean task displays
- 🔍 **Smart Search** - Find tasks by ID or title
- 🎯 **Priority Levels** - HIGH, MEDIUM, LOW with color coding

## 🏗️ Architecture

```
phase-I/
├── src/
│   ├── models/
│   │   └── task.py              # Task dataclass with validation
│   ├── repository/
│   │   └── task_repository.py     # In-memory storage (list-based)
│   ├── service/
│   │   └── task_service.py        # Business logic layer
│   └── cli/
│       ├── app.py                # Interactive CLI interface
│       └── __init__.py
├── pyproject.toml                   # Project configuration
├── main.py                         # Direct entry point wrapper
└── README.md                       # This file
```

**Design Patterns:**
- 🏛️ **Layered Architecture** - Separation of concerns (Model → Repository → Service → CLI)
- 📦 **Dependency Injection** - Service receives repository instance
- ✅ **Validation** - Business rules in model and service layers

## 📋 Features

### Core Operations

| Operation | Command | Description |
|------------|----------|-------------|
| ➕ **Add Task** | `add` | Create tasks with title, description, and priority |
| 📋 **List Tasks** | `list` | View all tasks in beautiful table format |
| 👁️ **View Task** | `get <id>` | Show detailed task information |
| ✅ **Complete** | `complete <id>` | Toggle task completion status |
| ✏️ **Update Task** | `update` | Modify task fields (ID or Title search) |
| 🗑️ **Delete Task** | `delete <id>` | Remove tasks permanently |
| ❓ **Help** | `help` | Display available commands |
| 👋 **Exit** | `exit` / `quit` | Leave interactive mode |

### Task Properties

- 🆔 **ID** - Auto-generated unique identifier
- 📝 **Title** - Required (1-200 characters)
- 📄 **Description** - Optional (0-1000 characters)
- 🎯 **Priority** - HIGH (🔴), MEDIUM (🟡), LOW (🟢)
- ⏰ **Created At** - Timestamp of task creation
- ✅ **Status** - Complete or Pending

## 🚀 Getting Started

### Prerequisites

- ✅ Python 3.13 or higher
- 💻 Windows, Linux, or macOS

### Installation

#### Option 1: Using Virtual Environment (Recommended)

```bash
# Navigate to phase-I directory
cd phase-I

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/macOS)
source .venv/bin/activate

# Install in development mode
pip install -e .
```

#### Option 2: Using UV (Fast)

```bash
cd phase-I
uv sync
```

### Running the Application

#### Method 1: Using Installed Command (Recommended)

```bash
cd phase-I
.venv\Scripts\todo        # Windows
./venv/bin/todo          # Linux/macOS
```

#### Method 2: Using Python Module

```bash
cd phase-I
python -m src.cli.app
```

#### Method 3: Direct Entry Point

```bash
cd phase-I
python main.py
```

## 📸 Usage Examples

### Adding a Task

```
🎨 todo> add

--- Add New Task ---
Task title: Complete project documentation
Description (optional, press Enter to skip): Update README and add inline comments
Priority (high/medium/low): high

✅ Task added with ID 1
     Title: Complete project documentation
     Priority: HIGH
```

### Viewing All Tasks

```
🎨 todo> list

=========================================================================================================
 ID | Title                       | Description                    | Status | Priority | Set Date
=========================================================================================================
  1 | Complete project documen... | Update README and add in...  | ✅     | HIGH       | 2026-01-01 10:30:45
  2 | Buy groceries               |                               | ⏳     | MEDIUM     | 2026-01-01 11:00:00
📊 Total Tasks: 2
```

### Updating a Task

```
🎨 todo> update

--- ✏️ Update Task ---
Enter Task ID or Title: 1

--- 📋 Current Task Details ---
ID: 1
Title: Complete project documentation
Description: Update README and add inline comments
Priority: HIGH
Status: ✅ Complete
Created: 2026-01-01 10:30:45

Press Enter to keep current value

New title [Complete project documentation]:
New description [Update README and add inline comments]:
New priority (high/medium/low) [high]: medium

✅ Task #1 updated successfully!
     New Title: Complete project documentation
     Priority: MEDIUM
```

### Searching Tasks by Title

```
🎨 todo> update
Enter Task ID or Title: documentation

🔍 Multiple tasks found matching 'documentation':
  1. [ID: 1] Complete project documentation
  2. [ID: 3] Write API documentation

Select task number (1-2): 1
```

## 🎨 UI/UX Features

### Color Scheme

| Element | Color | ANSI Code | Purpose |
|----------|--------|------------|---------|
| 🎨 **Banner** | Cyan | Welcome header and borders |
| ✅ **Success** | Green | Completed operations |
| ❌ **Error** | Red | Failed operations |
| ⚠️ **Warning** | Yellow | Alerts and invalid input |
| 🔴 **HIGH Priority** | Red | Urgent tasks |
| 🟡 **MEDIUM Priority** | Yellow | Normal tasks |
| 🟢 **LOW Priority** | Green | Low priority tasks |
| 📝 **Input Fields** | Blue | User prompts |

### Emoji Indicators

| State/Action | Emoji | Meaning |
|--------------|-------|---------|
| ✅ | Success / Complete |
| ❌ | Error / Failed |
| ⏳ | Pending task |
| 🚫 | Cancelled operation |
| ⚠️ | Warning / Invalid input |
| 🎯 | Welcome banner |
| 📊 | Task statistics |
| 📋 | List view |
| ✏️ | Update operation |
| 🗑️ | Delete operation |
| 👁️ | View/search |
| 🔍 | Multiple matches |
| 🎨 | Interactive prompt |

## ⚙️ Configuration

### Windows Console Support

The app automatically configures UTF-8 encoding on Windows to support emoji display:

```python
if sys.platform == 'win32':
    os.system('chcp 65001 > nul 2>&1')
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
```

## 📦 Project Structure

### Data Model

```python
@dataclass
class Task:
    id: int                          # Unique identifier
    title: str                        # Task name (required)
    description: str = ""              # Optional details
    priority: str = "medium"           # HIGH | MEDIUM | LOW
    completed: bool = False            # Completion status
    created_at: datetime                # Creation timestamp
```

### Service Layer

```python
class TaskService:
    create_task(title, description, priority)  # Create with validation
    list_tasks()                          # Get all tasks
    get_task(task_id)                      # Find by ID
    toggle_complete(task_id)                 # Mark complete/incomplete
    update_task(task_id, title, description) # Modify task
    delete_task(task_id)                    # Remove task
```

### Repository Layer

```python
class TaskRepository:
    add(task)           # Store new task
    get_all()           # Retrieve all tasks
    get_by_id(task_id)  # Find specific task
    update(task)         # Save changes
    delete(task_id)      # Remove task
```

## 🧪 Testing

### Manual Testing

Run the comprehensive manual test script:

```bash
cd phase-I
python test_manual.py
```

**Test Coverage:**
- ✅ Task creation with valid data
- ✅ Task creation with empty title (validation)
- ✅ Task retrieval by ID
- ✅ Task completion toggle
- ✅ Task update operations
- ✅ Task deletion
- ✅ Error handling for invalid inputs

## 🎯 Success Criteria

All acceptance criteria from specification have been met:

- ✅ **User can add tasks** with title and optional description
- ✅ **User can view all tasks** in formatted table
- ✅ **User can get task details** by ID
- ✅ **User can mark tasks complete/incomplete** (toggle)
- ✅ **User can update tasks** (title, description, priority)
- ✅ **User can delete tasks** by ID
- ✅ **Task IDs remain stable** during session (no duplicates)
- ✅ **Error messages clearly indicate** what went wrong
- ✅ **Console interface responds instantly** (<1 second)
- ✅ **Beautiful UI** with emojis and color coding

## 📊 Technical Details

| Aspect | Specification |
|----------|--------------|
| **Python Version** | 3.13+ |
| **Dependencies** | None (stdlib only) |
| **CLI Framework** | Custom interactive parser |
| **Storage** | In-memory list |
| **Character Encoding** | UTF-8 (auto-configured on Windows) |
| **Package Manager** | pip, UV compatible |

## 📝 Limitations

Current limitations by design for Phase I:

| Limitation | Impact | Future Phase |
|------------|-------|--------------|
| 🔴 **In-memory storage** | Tasks lost on exit | Phase II (SQLite) |
| 👤 **Single-user** | No authentication | Phase III |
| 📄 **No persistence** | No database/file storage | Phase II |
| 🔍 **No search/filter** | Can't filter tasks | Phase II |
| 🏷️ **No sorting** | Can't sort tasks | Phase II |
| 🏷️ **No priorities** | (Added in Phase I) | ✅ Already Added |
| 📅 **No due dates** | No reminders | Phase II |
| 🏷️ **No tags** | Can't categorize | Phase II |

## 🚀 Future Enhancements

**Phase II** will add:
- 💾 **Persistent Storage** - SQLite database integration
- 🔍 **Advanced Search** - Filter by status, priority, date
- 📅 **Due Dates** - Task deadlines and reminders
- 🏷️ **Task Tags** - Categorization support
- 📊 **Statistics** - Completion rates and charts

**Phase III** will add:
- 👥 **User Authentication** - Multi-user support
- ☁️ **Cloud Sync** - Cross-device synchronization
- 🌐 **Web Interface** - Browser-based todo manager

## 📜 License

This project is licensed under the **MIT License**.

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- 🐛 Report bugs
- 💡 Suggest features
- 📝 Submit pull requests

## 👨‍💻 Author

Built with ❤️ for "The Evolution of Todo" project

---

<div align="center">

  **Made with ❤️ and lots of 🎨**

</div>
