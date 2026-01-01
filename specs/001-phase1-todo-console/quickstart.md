# Quick Start Guide: Phase 1 - In-Memory Todo Console App

## Prerequisites

- Python 3.13 or higher
- UV package manager

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd The-Evolution-of-Todo

# Install dependencies (if using UV)
uv pip install -e .

# Or using pip
pip install -e .
```

## Running the Application

```bash
# Run from project root
python -m src.cli.main

# Or use the todo command (after installation)
todo --help
```

## Quick Verification

1. **Add a task**
   ```bash
   todo add "Buy groceries" --description "Milk, eggs, bread"
   ```

2. **List tasks**
   ```bash
   todo list
   ```

3. **Mark complete**
   ```bash
   todo complete 1
   ```

4. **Verify**
   ```bash
   todo list
   ```

5. **Clean up**
   ```bash
   todo delete 1
   ```

## Expected Output

After adding a task and listing:
```
ID | Status | Title
1  | [ ]    | Buy groceries
```

After marking complete:
```
Task #1 marked as complete
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Command not found | Ensure package is installed: `pip install -e .` |
| Python version error | Verify Python 3.13+: `python --version` |
| Task not found | Check task ID with `todo list` |
