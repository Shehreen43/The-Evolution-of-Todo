"""
Chat orchestration service for the AI Chatbot integration.
Handles the complete conversation flow with proper state management and tool integration.
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
import json
import logging
from datetime import datetime

from app.models.conversation import Conversation
from app.models.message import Message, MessageRole
from app.conversation_manager import create_conversation, get_conversation, get_conversation_history
from app.mcp.tools.add_task import handle_add_task
from app.mcp.tools.list_tasks import handle_list_tasks
from app.mcp.tools.update_task import handle_update_task
from app.mcp.tools.delete_task import handle_delete_task
from app.mcp.tools.complete_task import handle_complete_task
from app.mcp.tools.get_recurring_tasks import handle_get_recurring_tasks
from app.config import settings
from app.prompts import SYSTEM_PROMPT
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)

# Create a global variable to hold the client instance
_client_instance = None

def get_openai_client():
    """
    Get or create the OpenAI client instance.
    This ensures the client is only created when first needed, not at module import time.
    Prioritizes GROQ API if available, falls back to OpenRouter.
    """
    global _client_instance
    if _client_instance is None:
        # Prioritize GROQ if available
        if settings.groq_api_key:
            base_url = settings.groq_base_url or "https://api.groq.com/openai/v1"
            api_key = settings.groq_api_key
            print("Using GROQ API for AI service.")
        else:
            # Fallback to OpenRouter
            base_url = settings.openrouter_base_url or "https://openrouter.ai/api/v1"
            api_key = settings.openrouter_api_key

            if not api_key:
                print("WARNING: No AI API key set (neither GROQ nor OpenRouter). Streaming may not work.")

        _client_instance = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
        )
    return _client_instance


class ChatService:
    """Simplified chat service for basic chat functionality."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.orchestration_service = ChatOrchestrationService(db)

    async def process_chat(self, user_id: str, request):
        """
        Process a basic chat request and return the complete response.

        Args:
            user_id: User identifier
            request: ChatRequest object

        Returns:
            Complete response string
        """
        try:
            result = await self.orchestration_service.process_conversation(
                user_id,
                request.message,
                request.conversation_id
            )
            
            # Ensure we have a valid result tuple
            if result and isinstance(result, tuple) and len(result) >= 2:
                _, response, _ = result
                return response
            else:
                # If result is None or not a proper tuple, return an error message
                return "I'm sorry, but I encountered an error processing your request."
        except Exception as e:
            logger.error(f"Error in ChatService.process_chat: {str(e)}")
            return f"I'm sorry, but I encountered an error processing your request: {str(e)}"


class ChatOrchestrationService:
    """Service class to handle the complete chat orchestration flow."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute_tool_call(self, tool_call, user_id: str):
        """
        Execute a tool call from the AI response.

        Args:
            tool_call: Tool call object with name and arguments
            user_id: User identifier

        Returns:
            Result of the tool call
        """
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        # Add user_id to arguments for MCP tools
        arguments['user_id'] = user_id

        try:
            if tool_name == "add_task":
                return await handle_add_task(self.db, **arguments)
            elif tool_name == "list_tasks":
                return await handle_list_tasks(self.db, **arguments)
            elif tool_name == "update_task":
                return await handle_update_task(self.db, **arguments)
            elif tool_name == "delete_task":
                return await handle_delete_task(self.db, **arguments)
            elif tool_name == "complete_task":
                return await handle_complete_task(self.db, **arguments)
            elif tool_name == "get_recurring_tasks":
                return await handle_get_recurring_tasks(self.db, **arguments)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return {"error": f"Error executing {tool_name}: {str(e)}"}

    async def process_conversation(
        self,
        user_id: str,
        user_message: str,
        conversation_id: Optional[int] = None
    ):
        """
        Process a conversation turn with the AI assistant.

        Args:
            user_id: User identifier
            user_message: User's message input
            conversation_id: Existing conversation ID (None to create new)

        Returns:
            Tuple of (conversation_id, AI response, tool calls executed)
        """
        # Get or create conversation
        if conversation_id is None:
            # Create new conversation
            conversation = await create_conversation(self.db, user_id)
            conversation_id = conversation.id
            logger.info(f"Created new conversation {conversation_id} for user {user_id}")
        else:
            # Verify conversation belongs to user
            conversation = await get_conversation(self.db, conversation_id, user_id)
            if not conversation:
                raise ValueError("Conversation not found or unauthorized")

        # Save user message to database
        user_message_db = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=MessageRole.USER,
            content=user_message
        )
        self.db.add(user_message_db)
        await self.db.commit()
        await self.db.refresh(user_message_db)

        # Get conversation history for context
        messages_history = await get_conversation_history(self.db, conversation_id)

        # Prepare messages for the AI
        ai_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ]

        # Add historical messages
        for msg in messages_history:
            ai_messages.append({
                "role": msg.role.value if hasattr(msg.role, 'value') else msg.role,
                "content": msg.content
            })

        # Add the current user message
        ai_messages.append({"role": "user", "content": user_message})

        # Define tools for the AI
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task for the user. Use this when user wants to add, create, or remember something. Supports advanced features like due dates, reminders, categories, and recurring tasks.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Task title (required, max 200 characters)"
                            },
                            "description": {
                                "type": ["string", "null"],
                                "description": "Optional task description (max 1000 characters)"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "default": "medium",
                                "description": "Task priority level"
                            },
                            "due_date": {
                                "type": ["string", "null"],
                                "format": "date-time",
                                "description": "Due date for the task in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
                            },
                            "reminder_time": {
                                "type": ["string", "null"],
                                "format": "date-time",
                                "description": "Reminder time for the task in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
                            },
                            "category": {
                                "type": ["string", "null"],
                                "description": "Category or tag for the task (max 50 characters)"
                            },
                            "is_recurring": {
                                "type": "boolean",
                                "default": False,
                                "description": "Whether the task repeats"
                            },
                            "recurrence_pattern": {
                                "type": ["string", "null"],
                                "enum": ["daily", "weekly", "monthly", "yearly"],
                                "description": "Pattern for recurring tasks"
                            },
                            "end_recurrence": {
                                "type": ["string", "null"],
                                "format": "date-time",
                                "description": "End date for recurring tasks in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
                            }
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Retrieve a list of tasks for the user. Use this when user wants to see, view, or check their tasks. Supports filtering by status, category, due date, priority, and recurring status.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["all", "pending", "completed"],
                                "default": "all",
                                "description": "Filter tasks by completion status"
                            },
                            "category": {
                                "type": "string",
                                "description": "Filter tasks by category"
                            },
                            "due_date_filter": {
                                "type": "string",
                                "enum": ["all", "today", "overdue", "week", "month"],
                                "default": "all",
                                "description": "Filter tasks by due date (today, overdue, week, month)"
                            },
                            "is_recurring": {
                                "type": "boolean",
                                "description": "Filter tasks by recurring status (true/false)"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["all", "low", "medium", "high"],
                                "default": "all",
                                "description": "Filter tasks by priority"
                            },
                            "limit": {
                                "type": "integer",
                                "default": 10,
                                "description": "Maximum number of tasks to return"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task for the user. Supports updating advanced features like due dates, reminders, categories, and recurring settings.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "Task identifier to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New task title (max 200 characters)"
                            },
                            "description": {
                                "type": ["string", "null"],
                                "description": "New task description (max 1000 characters)"
                            },
                            "completed": {
                                "type": ["boolean", "null"],
                                "description": "New completion status"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "New task priority"
                            },
                            "due_date": {
                                "type": ["string", "null"],
                                "format": "date-time",
                                "description": "New due date for the task in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
                            },
                            "reminder_time": {
                                "type": ["string", "null"],
                                "format": "date-time",
                                "description": "New reminder time for the task in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
                            },
                            "category": {
                                "type": ["string", "null"],
                                "description": "New category or tag for the task (max 50 characters)"
                            },
                            "is_recurring": {
                                "type": ["boolean", "null"],
                                "description": "Whether the task should repeat"
                            },
                            "recurrence_pattern": {
                                "type": ["string", "null"],
                                "enum": ["daily", "weekly", "monthly", "yearly"],
                                "description": "New pattern for recurring tasks"
                            },
                            "end_recurrence": {
                                "type": ["string", "null"],
                                "format": "date-time",
                                "description": "New end date for recurring tasks in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task for the user.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": ["integer", "string"],
                                "description": "Task identifier to delete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed or incomplete for the user.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": ["integer", "string"],
                                "description": "Task identifier to update"
                            },
                            "completed": {
                                "type": ["boolean", "null"],
                                "default": True,
                                "description": "Whether the task is completed (true) or not (false)"
                            }
                        },
                        "required": ["task_id", "completed"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_recurring_tasks",
                    "description": "Retrieve a list of recurring tasks for the user. Use this when user wants to see, view, or check their recurring tasks.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["all", "active", "inactive"],
                                "default": "active",
                                "description": "Filter recurring tasks by status"
                            },
                            "limit": {
                                "type": "integer",
                                "default": 10,
                                "description": "Maximum number of tasks to return"
                            }
                        }
                    }
                }
            }
        ]

        try:
            # Call the AI with tools
            client = get_openai_client()

            # Check if API key is available
            if not settings.openrouter_api_key:
                logger.warning("OpenRouter API key not configured")
                # Return a helpful message to the user
                assistant_message = Message(
                    conversation_id=conversation_id,
                    user_id=user_id,
                    role=MessageRole.ASSISTANT,
                    content="I'm unable to process your request because the AI service is not configured. Please contact the administrator to set up the OpenRouter API key."
                )
                self.db.add(assistant_message)
                await self.db.commit()

                return conversation_id, "I'm unable to process your request because the AI service is not configured. Please contact the administrator to set up the OpenRouter API key.", []

            # First, try to call the AI with tools
            try:
                response = await client.chat.completions.create(
                    model=settings.default_model,
                    messages=ai_messages,
                    tools=tools,
                    tool_choice="auto",
                    max_tokens=1000,
                )
            except Exception as api_error:
                logger.error(f"API error in chat completion with tools: {str(api_error)}")

                # Check if it's a tool support error (common with free models)
                if "tool" in str(api_error).lower() or ("404" in str(api_error).lower() and "tool" in str(api_error).lower()):
                    logger.info(f"Model {settings.default_model} doesn't support tools, falling back to simple completion")
                    try:
                        # Try without tools
                        response = await client.chat.completions.create(
                            model=settings.default_model,
                            messages=ai_messages,
                            max_tokens=1000,
                        )
                        # Set a flag to indicate we're not using tools
                        tool_calls = []
                    except Exception as fallback_error:
                        logger.error(f"Simple completion also failed: {str(fallback_error)}")
                        # If simple completion fails too, try fallback models without tools
                        fallback_models = getattr(settings, 'fallback_models', None) or [getattr(settings, 'fallback_model', 'gryphe/mythomax-l2-13b:free')]

                        for fallback_model in fallback_models:
                            try:
                                logger.info(f"Trying fallback model without tools: {fallback_model}")
                                response = await client.chat.completions.create(
                                    model=fallback_model,
                                    messages=ai_messages,
                                    max_tokens=1000,
                                )
                                logger.info(f"Successfully used fallback model without tools: {fallback_model}")
                                break
                            except Exception as fallback_error2:
                                logger.error(f"Fallback model {fallback_model} also failed: {str(fallback_error2)}")
                                continue
                        else:
                            # All fallbacks failed
                            error_message = "I'm having trouble connecting to the AI service. The model may be unavailable. Please try again later."

                            assistant_message = Message(
                                conversation_id=conversation_id,
                                user_id=user_id,
                                role=MessageRole.ASSISTANT,
                                content=error_message
                            )
                            self.db.add(assistant_message)
                            await self.db.commit()

                            return conversation_id, error_message, []

                # Check if it's a rate limit error
                elif "rate limit" in str(api_error).lower() or "429" in str(api_error).lower():
                    # Handle rate limiting gracefully
                    rate_limit_message = "I'm currently experiencing high demand and need to limit my responses. Please try again in a moment, or consider upgrading to a premium plan for higher limits."

                    assistant_message = Message(
                        conversation_id=conversation_id,
                        user_id=user_id,
                        role=MessageRole.ASSISTANT,
                        content=rate_limit_message
                    )
                    self.db.add(assistant_message)
                    await self.db.commit()

                    return conversation_id, rate_limit_message, []

                # Check if it's an invalid model error
                elif "model" in str(api_error).lower():
                    # Try with fallback models if the default model fails
                    fallback_models = getattr(settings, 'fallback_models', None) or [getattr(settings, 'fallback_model', 'meta-llama/llama-3.3-70b-instruct:free')]

                    for fallback_model in fallback_models:
                        try:
                            logger.info(f"Trying fallback model: {fallback_model}")
                            # First try with tools
                            try:
                                response = await client.chat.completions.create(
                                    model=fallback_model,
                                    messages=ai_messages,
                                    tools=tools,
                                    tool_choice="auto",
                                    max_tokens=1000,
                                )
                            except:
                                # If tools fail, try without tools
                                logger.info(f"Model {fallback_model} doesn't support tools, trying without tools")
                                response = await client.chat.completions.create(
                                    model=fallback_model,
                                    messages=ai_messages,
                                    max_tokens=1000,
                                )
                            logger.info(f"Successfully used fallback model: {fallback_model}")
                            break
                        except Exception as fallback_error:
                            logger.error(f"Fallback model {fallback_model} also failed: {str(fallback_error)}")
                            continue
                    else:
                        # All fallbacks failed
                        error_message = "I'm having trouble connecting to the AI service. The model may be unavailable. Please try again later."

                        assistant_message = Message(
                            conversation_id=conversation_id,
                            user_id=user_id,
                            role=MessageRole.ASSISTANT,
                            content=error_message
                        )
                        self.db.add(assistant_message)
                        await self.db.commit()

                        return conversation_id, error_message, []
                else:
                    # Re-raise other API errors
                    raise api_error

            # Process the response
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls if hasattr(response_message, 'tool_calls') else []

            # Execute tool calls if any
            executed_tool_calls = []
            if tool_calls:
                for tool_call in tool_calls:
                    # Execute the tool
                    result = await self.execute_tool_call(tool_call, user_id)

                    # Save tool call as a message in the database
                    tool_message = Message(
                        conversation_id=conversation_id,
                        user_id=user_id,
                        role=MessageRole.TOOL,
                        content=json.dumps(result),
                        tool_calls=json.dumps({
                            "name": tool_call.function.name,
                            "arguments": json.loads(tool_call.function.arguments)
                        })
                    )
                    self.db.add(tool_message)
                    await self.db.commit()  # Commit immediately to ensure the tool call is saved

                    executed_tool_calls.append({
                        "tool": tool_call.function.name,
                        "arguments": json.loads(tool_call.function.arguments),
                        "result": result
                    })

                # Submit the tool results to get the final response
                if executed_tool_calls:
                    # Get the final response from the AI using the original client
                    final_response = await client.chat.completions.create(
                        model=settings.default_model,
                        messages=ai_messages + [
                            {
                                "role": "assistant",
                                "content": response_message.content,  # Include original content if available
                                "tool_calls": [
                                    {
                                        "id": getattr(tc, 'id', f"call_{int(datetime.now().timestamp())}"),  # Generate ID if not present
                                        "function": {
                                            "arguments": tc.function.arguments,
                                            "name": tc.function.name,
                                        },
                                        "type": "function",
                                    } for tc in tool_calls
                                ]
                            }
                        ] + [
                            {
                                "role": "tool",
                                "content": json.dumps(executed_tool_calls[i]["result"]),
                                "tool_call_id": getattr(tool_calls[i], 'id', f"call_{int(datetime.now().timestamp())}")
                            } for i in range(len(tool_calls))
                        ],
                        max_tokens=500,
                    )
                    final_content = final_response.choices[0].message.content
                else:
                    final_content = response_message.content or "I processed your request."
            else:
                # No tool calls, just return the content
                final_content = response_message.content or "I processed your request."

            # Save assistant response to database
            assistant_message = Message(
                conversation_id=conversation_id,
                user_id=user_id,
                role=MessageRole.ASSISTANT,
                content=final_content or "I processed your request."
            )
            self.db.add(assistant_message)
            await self.db.commit()

            return conversation_id, final_content or "I processed your request.", executed_tool_calls

        except Exception as e:
            logger.error(f"Error in chat orchestration: {str(e)}")
            
            # Create an error message for the user
            error_message = f"I'm sorry, but I encountered an error processing your request: {str(e)}"
            
            # Save error message to database
            assistant_message = Message(
                conversation_id=conversation_id,
                user_id=user_id,
                role=MessageRole.ASSISTANT,
                content=error_message
            )
            self.db.add(assistant_message)
            await self.db.commit()
            
            # Return the expected tuple to prevent the 'NoneType' error
            return conversation_id, error_message, []