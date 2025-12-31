"""CLI entry point for Phase I Todo Console App."""

import argparse
import sys
from src.models.task import Task
from src.repository.task_repository import TaskRepository
from src.service.task_service import TaskService


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser with all subcommands.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog="todo",
        description="Phase I - In-Memory Todo Console Application"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="Todo Console App v1.0.0"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # User Story 1: Add task
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Task title (1-200 characters)")
    add_parser.add_argument("--description", type=str, default="", help="Task description (0-1000 characters)")

    # User Story 2: List tasks
    subparsers.add_parser("list", help="View all tasks")

    # User Story 2: Get specific task
    get_parser = subparsers.add_parser("get", help="View a specific task")
    get_parser.add_argument("id", type=int, help="Task ID")

    # User Story 3: Mark complete
    complete_parser = subparsers.add_parser("complete", help="Mark task as complete/incomplete (toggle)")
    complete_parser.add_argument("id", type=int, help="Task ID")

    # User Story 4: Delete task
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    # User Story 5: Update task
    update_parser = subparsers.add_parser("update", help="Update task details")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("--title", type=str, help="New task title")
    update_parser.add_argument("--description", type=str, help="New task description")

    return parser


def handle_add(service: TaskService, args) -> int:
    """Handle 'add' command - User Story 1.

    Args:
        service: TaskService instance
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        task = service.create_task(title=args.title, description=args.description)
        print(f"Task added with ID {task.id}")
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_list(service: TaskService, args) -> int:
    """Handle 'list' command - User Story 2.

    Args:
        service: TaskService instance
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success)
    """
    tasks = service.list_tasks()

    if not tasks:
        print("No tasks found. Add a task to get started.")
        return 0

    # Format table output
    print("ID | Status | Title")
    for task in tasks:
        status = "[x]" if task.completed else "[ ]"
        print(f"{task.id}  | {status}    | {task.title}")

    return 0


def handle_get(service: TaskService, args) -> int:
    """Handle 'get' command - User Story 2.

    Args:
        service: TaskService instance
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    task = service.get_task(args.id)

    if not task:
        print(f"Error: Task with ID {args.id} not found", file=sys.stderr)
        return 1

    # Format detailed output
    status = "Complete" if task.completed else "Pending"
    print(f"Task #{task.id}")
    print(f"Title: {task.title}")
    print(f"Description: {task.description}")
    print(f"Status: {status}")
    print(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

    return 0


def handle_complete(service: TaskService, args) -> int:
    """Handle 'complete' command - User Story 3.

    Args:
        service: TaskService instance
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        task = service.toggle_complete(args.id)
        status = "complete" if task.completed else "incomplete"
        print(f"Task #{task.id} marked as {status}")
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def handle_delete(service: TaskService, args) -> int:
    """Handle 'delete' command - User Story 4.

    Args:
        service: TaskService instance
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    success = service.delete_task(args.id)

    if success:
        print(f"Task #{args.id} deleted")
        return 0
    else:
        print(f"Error: Task with ID {args.id} not found", file=sys.stderr)
        return 1


def handle_update(service: TaskService, args) -> int:
    """Handle 'update' command - User Story 5.

    Args:
        service: TaskService instance
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Validate at least one field is provided
    if args.title is None and args.description is None:
        print("Error: At least one of --title or --description must be provided", file=sys.stderr)
        return 1

    try:
        service.update_task(
            task_id=args.id,
            title=args.title,
            description=args.description
        )
        print(f"Task #{args.id} updated")
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def main():
    """Main entry point for the CLI application."""
    # Initialize components
    repository = TaskRepository()
    service = TaskService(repository)

    # Parse arguments
    parser = create_parser()
    args = parser.parse_args()

    # Handle commands
    if args.command == "add":
        sys.exit(handle_add(service, args))
    elif args.command == "list":
        sys.exit(handle_list(service, args))
    elif args.command == "get":
        sys.exit(handle_get(service, args))
    elif args.command == "complete":
        sys.exit(handle_complete(service, args))
    elif args.command == "delete":
        sys.exit(handle_delete(service, args))
    elif args.command == "update":
        sys.exit(handle_update(service, args))
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
