"""
MCP Tools Package
Contains all the Model Context Protocol tools for the Todo AI Chatbot.
"""
from .add_task import ADD_TASK_TOOL, handle_add_task
from .list_tasks import LIST_TASKS_TOOL, handle_list_tasks
from .update_task import UPDATE_TASK_TOOL, handle_update_task
from .delete_task import DELETE_TASK_TOOL, handle_delete_task
from .complete_task import COMPLETE_TASK_TOOL, handle_complete_task
from .get_recurring_tasks import GET_RECURRING_TASKS_TOOL, handle_get_recurring_tasks

__all__ = [
    "ADD_TASK_TOOL",
    "LIST_TASKS_TOOL",
    "UPDATE_TASK_TOOL",
    "DELETE_TASK_TOOL",
    "COMPLETE_TASK_TOOL",
    "GET_RECURRING_TASKS_TOOL",
    "handle_add_task",
    "handle_list_tasks",
    "handle_update_task",
    "handle_delete_task",
    "handle_complete_task",
    "handle_get_recurring_tasks"
]