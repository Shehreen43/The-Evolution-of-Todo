"""CLI entry point for Phase I Todo Console App - Interactive Mode Only."""

import sys
import os

# Set UTF-8 encoding for Windows console to support emojis
if sys.platform == 'win32':
    # Set console to UTF-8
    os.system('chcp 65001 > nul 2>&1')
    # Set Python output encoding
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
from src.models.task import Task
from src.repository.task_repository import TaskRepository
from src.service.task_service import TaskService

# ANSI color codes for colorful console output
class Colors:
    """ANSI escape codes for terminal colors."""
    RESET = '\033[0m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'


def print_banner():
    """Print H1-size welcome banner for interactive mode."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║ {Colors.GREEN}██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗{Colors.CYAN}   ║
║ {Colors.GREEN}██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝{Colors.CYAN}   ║
║ {Colors.GREEN}██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗  {Colors.CYAN}   ║
║ {Colors.GREEN}██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝  {Colors.CYAN}   ║
║ {Colors.GREEN}╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗{Colors.CYAN}   ║
║ {Colors.GREEN} ╚═╝ ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝       ╚═╝╚══════╝{Colors.CYAN}   ║
║                                                                                             ║
║ {Colors.MAGENTA}████████╗ ██████╗     ████████╗ ██████╗ ██████╗  █████╗{Colors.CYAN}        ║
║ {Colors.MAGENTA}╚══██╔══╝██╔═══██╗    ╚══██╔══╝██╔═══██╗██╔═  ██╗██╔══██╗{Colors.CYAN}      ║
║ {Colors.MAGENTA}   ██║   ██║   ██║       ██║   ██║   ██║██║   ██║██   ██║{Colors.CYAN}      ║
║ {Colors.MAGENTA}   ██║   ██║   ██║       ██║   ██║   ██║██║   ██║██╔══██║{Colors.CYAN}      ║
║ {Colors.MAGENTA}   ██║   ╚██████╔╝       ██║   ╚██████╔╝██████ ╔╝ █████║{Colors.CYAN}       ║
║ {Colors.MAGENTA}   ╚═╝    ╚═════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝{Colors.CYAN}      ║
║                                                                                             ║                                           ║
║ {Colors.YELLOW} Interactive Console Mode v1.0.0{Colors.CYAN}                                ║
║ {Colors.YELLOW} Type 'help' for commands | 'exit' to quit{Colors.CYAN}                      ║
║                                                                                             ║
╚═════════════════════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}
"""
    print(banner)


def print_interactive_help():
    """Print available commands in interactive mode."""
    help_text = f"""
{Colors.CYAN}Available Commands:{Colors.RESET}
  {Colors.GREEN}➕ add{Colors.RESET}                - Add a new task (guided prompts)
  {Colors.GREEN}📋 list{Colors.RESET}               - View all tasks in table format
  {Colors.GREEN}👁️  Search{Colors.RESET} <id>       - View task details
  {Colors.GREEN}✅ complete{Colors.RESET} <id>      - Toggle task completion
  {Colors.GREEN}✏️  update{Colors.RESET}            - Update task by ID or Title (guided prompts)
  {Colors.GREEN}🗑️  delete{Colors.RESET} <id>       - Delete a task
  {Colors.GREEN}❓ help{Colors.RESET}                - Show this help
  {Colors.GREEN}👋 exit{Colors.RESET} / {Colors.GREEN}quit{Colors.RESET}      - Exit interactive mode
"""
    print(help_text)


def interactive_add_guided(service: TaskService):
    """Handle 'add' command with guided prompts for title, description, and priority.

    Prompts user step-by-step:
    1. Task title (required)
    2. Description (optional, press Enter to skip)
    3. Priority (high/medium/low, defaults to medium)
    """
    try:
        # Step 1: Prompt for title (required)
        print(f"\n{Colors.CYAN}--- Add New Task ---{Colors.RESET}")
        title = input(f"{Colors.BLUE}Task title:{Colors.RESET} ").strip()

        if not title:
            print(f"{Colors.RED}❌ Error: Title cannot be empty{Colors.RESET}")
            return

        # Step 2: Prompt for description (optional)
        description = input(f"{Colors.BLUE}Description (optional, press Enter to skip):{Colors.RESET} ").strip()

        # Step 3: Prompt for priority with default
        print(f"{Colors.BLUE}Priority (high/medium/low):{Colors.RESET} ", end="")
        priority_input = input().strip().lower()

        # Default to 'medium' if empty or invalid
        if not priority_input or priority_input not in ['high', 'medium', 'low']:
            priority = 'medium'
            if priority_input and priority_input not in ['high', 'medium', 'low']:
                print(f"{Colors.YELLOW}⚠️ Invalid priority. Defaulting to 'medium'.{Colors.RESET}")
        else:
            priority = priority_input

        # Create the task
        task = service.create_task(title=title, description=description, priority=priority)

        # Display priority with color coding
        priority_display = {
            'high': f"{Colors.RED}HIGH{Colors.RESET}",
            'medium': f"{Colors.YELLOW}MEDIUM{Colors.RESET}",
            'low': f"{Colors.GREEN}LOW{Colors.RESET}"
        }

        print(f"\n{Colors.GREEN}✅ Task added with ID {task.id}{Colors.RESET}")
        print(f"     Title: {task.title}")
        print(f"     Priority: {priority_display[task.priority]}\n")

    except ValueError as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🚫 Task creation cancelled.{Colors.RESET}")


def interactive_list(service: TaskService):
    """Handle 'list' command - displays all tasks in clean table format.

    Displays tasks with: ID, Title, Description, Status, Priority, Set Date
    Includes header, body, and footer with total count.
    """
    tasks = service.list_tasks()

    if not tasks:
        print(f"\n{Colors.YELLOW}📭 No tasks found. Use 'add' to create your first task.{Colors.RESET}\n")
        return

    # Priority color mapping
    priority_colors = {
        'high': Colors.RED,
        'medium': Colors.YELLOW,
        'low': Colors.GREEN
    }

    # Define column widths for alignment
    col_id = 4
    col_title = 25
    col_description = 30
    col_status = 8
    col_priority = 10
    col_date = 20

    # Helper function to truncate text with ellipsis
    def truncate(text, width):
        """Truncate text to fit column width, add ... if needed."""
        if len(text) <= width:
            return text.ljust(width)
        return text[:width-3] + "..."

    # Print table header
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'=' * (col_id + col_title + col_description + col_status + col_priority + col_date + 15)}{Colors.RESET}")
    header = f"{Colors.CYAN}{Colors.BOLD}{'ID'.center(col_id)} | {'Title'.ljust(col_title)} | {'Description'.ljust(col_description)} | {'Status'.center(col_status)} | {'Priority'.center(col_priority)} | {'Set Date'.ljust(col_date)}{Colors.RESET}"
    print(header)
    print(f"{Colors.CYAN}{'=' * (col_id + col_title + col_description + col_status + col_priority + col_date + 15)}{Colors.RESET}")

    # Print table body (tasks)
    for task in tasks:
        # Format each column
        task_id = f"{Colors.BLUE}{str(task.id).center(col_id)}{Colors.RESET}"

        # Truncate title if too long
        title_text = truncate(task.title, col_title)

        # Handle empty description
        description_text = task.description if task.description else "None"
        description_text = truncate(description_text, col_description)

        # Status with color
        if task.completed:
            status = f"{Colors.GREEN}{'✅'.center(col_status)}{Colors.RESET}"
        else:
            status = f"{Colors.YELLOW}{'⏳'.center(col_status)}{Colors.RESET}"

        # Priority with color
        priority_color = priority_colors.get(task.priority, Colors.RESET)
        priority_text = f"{priority_color}{task.priority.upper().center(col_priority)}{Colors.RESET}"

        # Format date
        date_text = task.created_at.strftime('%Y-%m-%d %H:%M:%S').ljust(col_date)

        # Print row
        print(f"{task_id} | {title_text} | {description_text} | {status} | {priority_text} | {date_text}")

    # Print table footer
    print(f"{Colors.CYAN}{'=' * (col_id + col_title + col_description + col_status + col_priority + col_date + 15)}{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}📊 Total Tasks: {len(tasks)}{Colors.RESET}")
    print()


def interactive_get(service: TaskService, parts: list):
    """Handle 'get' command - displays detailed task information including priority."""
    if len(parts) < 2:
        print(f"{Colors.RED}❌ Error: Task ID required{Colors.RESET}")
        print(f"{Colors.YELLOW}Usage: get <id>{Colors.RESET}")
        return

    try:
        task_id = int(parts[1])
    except ValueError:
        print(f"{Colors.RED}❌ Error: ID must be a number{Colors.RESET}")
        return

    task = service.get_task(task_id)

    if not task:
        print(f"{Colors.RED}❌ Error: Task with ID {task_id} not found{Colors.RESET}")
        return

    # Priority color mapping
    priority_colors = {
        'high': f"{Colors.RED}HIGH{Colors.RESET}",
        'medium': f"{Colors.YELLOW}MEDIUM{Colors.RESET}",
        'low': f"{Colors.GREEN}LOW{Colors.RESET}"
    }

    # Format detailed output with colors
    status = f"{Colors.GREEN}✅ Complete{Colors.RESET}" if task.completed else f"{Colors.YELLOW}⏳ Pending{Colors.RESET}"
    print(f"\n{Colors.CYAN}{Colors.BOLD}📝 Task #{task.id}{Colors.RESET}")
    print(f"{Colors.BLUE}Title:{Colors.RESET} {task.title}")
    print(f"{Colors.BLUE}Description:{Colors.RESET} {task.description if task.description else '(none)'}")
    print(f"{Colors.BLUE}Priority:{Colors.RESET} {priority_colors[task.priority]}")
    print(f"{Colors.BLUE}Status:{Colors.RESET} {status}")
    print(f"{Colors.BLUE}Created:{Colors.RESET} {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n")


def interactive_complete(service: TaskService, parts: list):
    """Handle 'complete' command - toggles task completion status."""
    if len(parts) < 2:
        print(f"{Colors.RED}❌ Error: Task ID required{Colors.RESET}")
        print(f"{Colors.YELLOW}Usage: complete <id>{Colors.RESET}")
        return

    try:
        task_id = int(parts[1])
    except ValueError:
        print(f"{Colors.RED}❌ Error: ID must be a number{Colors.RESET}")
        return

    try:
        task = service.toggle_complete(task_id)
        status = "✅ complete" if task.completed else "⏳ incomplete"
        print(f"{Colors.GREEN}🔄 Task #{task.id} marked as {status}{Colors.RESET}")
    except ValueError as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")


def interactive_update_guided(service: TaskService, parts: list):
    """Handle 'update' command with fully interactive prompts.

    Prompts user to identify task by ID or Title, then updates each field.
    """
    print(f"\n{Colors.CYAN}          --- ✏️ Update Task ---{Colors.RESET}\n")

    # Step 1: Identify task by ID or Title (no ID required in command)
    try:
        identifier = input(f"{Colors.BLUE}Enter Task ID or Title:{Colors.RESET} ").strip()

        if not identifier:
            print(f"{Colors.RED}❌ Error: Task ID or Title is required{Colors.RESET}")
            return

        # Try to parse as ID first
        task = None
        try:
            task_id = int(identifier)
            task = service.get_task(task_id)
        except ValueError:
            # Not a number, search by title
            all_tasks = service.list_tasks()
            # Case-insensitive partial match
            matching_tasks = [t for t in all_tasks if identifier.lower() in t.title.lower()]

            if len(matching_tasks) == 0:
                print(f"{Colors.RED}❌ Task not found. Please check the ID or Title and try again.{Colors.RESET}")
                return
            elif len(matching_tasks) == 1:
                task = matching_tasks[0]
            else:
                # Multiple matches - show list and ask user to select
                print(f"\n{Colors.YELLOW}🔍 Multiple tasks found matching '{identifier}':{Colors.RESET}")
                for i, t in enumerate(matching_tasks, 1):
                    print(f"  {i}. [ID: {t.id}] {t.title}")

                choice = input(f"{Colors.BLUE}Select task number (1-{len(matching_tasks)}):{Colors.RESET} ").strip()
                try:
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(matching_tasks):
                        task = matching_tasks[choice_idx]
                    else:
                        print(f"{Colors.RED}❌ Invalid selection{Colors.RESET}")
                        return
                except ValueError:
                    print(f"{Colors.RED}❌ Invalid selection{Colors.RESET}")
                    return

        # If still no task found by ID
        if not task:
            print(f"{Colors.RED}❌ Task not found. Please check the ID or Title and try again.{Colors.RESET}")
            return

        # Step 2: Show current task details
        status = f"{Colors.GREEN}✅ Complete{Colors.RESET}" if task.completed else f"{Colors.YELLOW}⏳ Pending{Colors.RESET}"
        print(f"\n{Colors.CYAN}--- 📋 Current Task Details ---{Colors.RESET}\n")
        print(f"{Colors.BLUE}ID: {Colors.RESET} {task.id}")
        print(f"{Colors.BLUE}Title: {Colors.RESET} {task.title}")
        print(f"{Colors.BLUE}Description: {Colors.RESET} {task.description if task.description else '(none)'}")
        print(f"{Colors.BLUE}Priority: {Colors.RESET} {task.priority.upper()}")
        print(f"{Colors.BLUE}Status: {Colors.RESET} {status}")
        print(f"{Colors.YELLOW}\nPress Enter to keep current value{Colors.RESET}\n")

        # Step 3: Prompt for each field update.
        # Update title
        new_title = input(f"{Colors.BLUE}New title [{task.title}]:{Colors.RESET} ").strip()
        if not new_title:
            new_title = None  # Keep current

        # Update description
        current_desc = task.description if task.description else "(none)"
        new_description = input(f"{Colors.BLUE}New description [{current_desc}]:{Colors.RESET} ").strip()
        if not new_description:
            new_description = None  # Keep current

        # Update priority
        print(f"{Colors.BLUE}New priority (high/medium/low) [{task.priority}]:{Colors.RESET} ", end="")
        new_priority = input().strip().lower()
        if not new_priority:
            new_priority = None  # Keep current
        elif new_priority not in ['high', 'medium', 'low']:
            print(f"{Colors.YELLOW}⚠️ Invalid priority. Keeping current value.{Colors.RESET}")
            new_priority = None

        # Step 4: Apply updates if any field changed
        if new_title is not None or new_description is not None or new_priority is not None:
            # Update fields
            if new_title:
                task.title = new_title
            if new_description:
                task.description = new_description
            if new_priority:
                task.priority = new_priority

            # Re-validate
            task._validate_title()
            task._validate_description()
            task._validate_priority()

            # Save via repository
            service._repository.update(task)
            print(f"\n{Colors.GREEN}✅ Task #{task.id} updated successfully!{Colors.RESET}")
            print(f"     New Title: {task.title}")
            print(f"     Priority: {task.priority.upper()}\n")
        else:
            print(f"\n{Colors.YELLOW}🚫 No changes made.{Colors.RESET}\n")

    except ValueError as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}🚫 Update cancelled.{Colors.RESET}")


def interactive_delete(service: TaskService, parts: list):
    """Handle 'delete' command - removes a task by ID."""
    if len(parts) < 2:
        print(f"{Colors.RED}❌ Error: Task ID required{Colors.RESET}")
        print(f"{Colors.YELLOW}Usage: delete <id>{Colors.RESET}")
        return

    try:
        task_id = int(parts[1])
    except ValueError:
        print(f"{Colors.RED}❌ Error: ID must be a number{Colors.RESET}")
        return

    success = service.delete_task(task_id)

    if success:
        print(f"{Colors.GREEN}🗑️ Task #{task_id} deleted{Colors.RESET}")
    else:
        print(f"{Colors.RED}❌ Error: Task with ID {task_id} not found{Colors.RESET}")


def run_interactive_mode(service: TaskService):
    """Run the interactive REPL loop.

    App starts immediately in interactive mode.
    Tasks remain in memory until user exits.
    All commands are available via simple text input.
    """
    print_banner()
    print_interactive_help()

    while True:
        try:
            # Show colorful prompt
            user_input = input(f"{Colors.BLUE}🎨 todo> {Colors.RESET}").strip()

            if not user_input:
                continue

            # Parse input manually
            parts = user_input.split()
            command = parts[0].lower()

            # Dispatch to appropriate handler
            if command in ["exit", "quit"]:
                print(f"{Colors.CYAN}👋 Goodbye! Your tasks were stored in memory only.{Colors.RESET}")
                break
            elif command == "help":
                print_interactive_help()
            elif command == "add":
                # Guided add with prompts
                interactive_add_guided(service)
            elif command == "list":
                interactive_list(service)
            elif command == "get":
                interactive_get(service, parts)
            elif command == "complete":
                interactive_complete(service, parts)
            elif command == "update":
                # Guided update with prompts
                interactive_update_guided(service, parts)
            elif command == "delete":
                interactive_delete(service, parts)
            else:
                print(f"{Colors.RED}❓ Unknown command: {command}{Colors.RESET}")
                print(f"{Colors.YELLOW}Type 'help' for available commands{Colors.RESET}")

        except KeyboardInterrupt:
            print(f"\n{Colors.CYAN}ℹ️ Use 'exit' or 'quit' to leave interactive mode{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}💥 Unexpected error: {e}{Colors.RESET}")


def main():
    """Main entry point - starts interactive mode immediately."""
    # Initialize components
    repository = TaskRepository()
    service = TaskService(repository)

    # Start interactive mode immediately (no flags needed)
    run_interactive_mode(service)


if __name__ == "__main__":
    main()
