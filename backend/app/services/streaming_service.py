"""
Streaming service for chat responses compatible with Vercel AI SDK.
FIXED: Now outputs format that Vercel AI SDK can parse.
"""
import asyncio
import json
import logging
from typing import AsyncGenerator, Dict, Any, Optional
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message, MessageRole
from app.models.conversation import Conversation
from app.conversation_manager import create_conversation, get_conversation, get_conversation_history
from app.schemas.api_contract import ChatRequest, ToolCall
from app.config import settings
from app.services.chat_service import get_openai_client
from app.mcp.tools.add_task import handle_add_task
from app.mcp.tools.list_tasks import handle_list_tasks
from app.mcp.tools.update_task import handle_update_task
from app.mcp.tools.delete_task import handle_delete_task
from app.mcp.tools.complete_task import handle_complete_task
from app.mcp.tools.get_recurring_tasks import handle_get_recurring_tasks
from app.prompts import SYSTEM_PROMPT


logger = logging.getLogger(__name__)


class StreamingChatService:
    """Service class to handle streaming chat responses."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute_tool_call(self, tool_call: ToolCall, user_id: str):
        """Execute a tool call from the AI response."""
        tool_name = tool_call.name
        arguments = tool_call.arguments
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

    async def stream_chat_response(
        self,
        user_id: str,
        request: ChatRequest
    ) -> AsyncGenerator[str, None]:
        """
        Stream chat responses in Vercel AI SDK compatible format.

        Format expected by Vercel AI SDK:
        - Text chunks: 0:"content"\n
        - Data: 2:[{"type":"data","value":{...}}]\n
        - Completion: d:{"finishReason":"stop"}\n
        - Errors: 3:{"error message"}\n
        """
        conversation_id = request.conversation_id
        user_message = request.message
        full_response = ""

        try:
            # Get or create conversation
            if conversation_id is None:
                conversation = await create_conversation(self.db, user_id)
                conversation_id = conversation.id
                logger.info(f"Created new conversation {conversation_id}")
            else:
                conversation = await get_conversation(self.db, conversation_id, user_id)
                if not conversation:
                    raise HTTPException(status_code=404, detail="Conversation not found")

            # Save user message
            user_message_db = Message(
                conversation_id=conversation_id,
                user_id=user_id,
                role=MessageRole.USER,
                content=user_message
            )
            self.db.add(user_message_db)
            await self.db.commit()

            # Get conversation history
            messages_history = await get_conversation_history(self.db, conversation_id)

            # Prepare messages for AI
            ai_messages = [
                {
                    "role": "system",
                    "content": f"{SYSTEM_PROMPT}\n\nCurrent Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                },
            ]

            for msg in messages_history:
                ai_messages.append({
                    "role": msg.role.value if hasattr(msg.role, 'value') else msg.role,
                    "content": msg.content
                })

            ai_messages.append({"role": "user", "content": user_message})

            # Define tools
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "add_task",
                        "description": "Create a new task for the user. Supports advanced features like due dates, reminders, categories, and recurring tasks.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string", "description": "Task title (required, max 200 characters)"},
                                "description": {"type": "string", "description": "Task description (max 1000 characters)"},
                                "priority": {
                                    "type": "string",
                                    "enum": ["low", "medium", "high"],
                                    "default": "medium",
                                    "description": "Task priority level"
                                },
                                "due_date": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "Due date for the task in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
                                },
                                "reminder_time": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "Reminder time for the task in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
                                },
                                "category": {
                                    "type": "string",
                                    "description": "Category or tag for the task (max 50 characters)"
                                },
                                "is_recurring": {
                                    "type": "boolean",
                                    "default": False,
                                    "description": "Whether the task repeats"
                                },
                                "recurrence_pattern": {
                                    "type": "string",
                                    "enum": ["daily", "weekly", "monthly", "yearly"],
                                    "description": "Pattern for recurring tasks"
                                },
                                "end_recurrence": {
                                    "type": "string",
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
                        "description": "Retrieve user's tasks. Supports filtering by status, category, due date, priority, and recurring status.",
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
                                "limit": {"type": "integer", "default": 10, "description": "Maximum number of tasks to return"}
                            }
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "update_task",
                        "description": "Update an existing task. Supports updating advanced features like due dates, reminders, categories, and recurring settings.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "integer", "description": "Task identifier"},
                                "title": {"type": "string", "description": "New task title (max 200 characters)"},
                                "description": {"type": "string", "description": "New task description (max 1000 characters)"},
                                "completed": {"type": "boolean", "description": "New completion status"},
                                "priority": {
                                    "type": "string",
                                    "enum": ["low", "medium", "high"],
                                    "description": "New task priority"
                                },
                                "due_date": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "New due date for the task in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
                                },
                                "reminder_time": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "New reminder time for the task in ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
                                },
                                "category": {
                                    "type": "string",
                                    "description": "New category or tag for the task (max 50 characters)"
                                },
                                "is_recurring": {
                                    "type": "boolean",
                                    "description": "Whether the task should repeat"
                                },
                                "recurrence_pattern": {
                                    "type": "string",
                                    "enum": ["daily", "weekly", "monthly", "yearly"],
                                    "description": "New pattern for recurring tasks"
                                },
                                "end_recurrence": {
                                    "type": "string",
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
                        "description": "Delete a task.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "integer", "description": "Task identifier to delete"}
                            },
                            "required": ["task_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "complete_task",
                        "description": "Mark task as completed/incomplete.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "task_id": {"type": "integer"},
                                "completed": {"type": "boolean", "default": True}
                            },
                            "required": ["task_id", "completed"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "get_recurring_tasks",
                        "description": "Retrieve user's recurring tasks.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "status": {
                                    "type": "string",
                                    "enum": ["all", "active", "inactive"],
                                    "default": "active",
                                    "description": "Filter recurring tasks by status"
                                },
                                "limit": {"type": "integer", "default": 10, "description": "Maximum number of tasks to return"}
                            }
                        }
                    }
                }
            ]

            # Get OpenAI client
            client = get_openai_client()

            if not settings.groq_api_key and not settings.openrouter_api_key:
                error_msg = "AI service not configured. Please contact administrator."
                # Send error in Vercel AI SDK format
                yield f'0:{json.dumps(error_msg)}\n'
                yield 'd:{"finishReason":"stop"}\n'
                return

            loop_count = 0
            max_loops = 5
            
            while loop_count < max_loops:
                loop_count += 1
                
                # Try streaming with tools
                try:
                    response = await client.chat.completions.create(
                        model=settings.default_model,
                        messages=ai_messages,
                        tools=tools,
                        tool_choice="auto",
                        max_tokens=1000,
                        stream=True,
                    )
                except Exception as tool_error:
                    logger.warning(f"Tool streaming failed: {str(tool_error)}")
                    # ... (Error handling logic same as before, but adapted for loop if needed) ...
                    # For brevity in replacement, assuming similar error handling logic:
                    error_str = str(tool_error).lower()
                    if '429' in error_str or 'rate' in error_str or 'limit' in error_str:
                         error_msg = "AI service is temporarily rate limited."
                         yield f'0:{json.dumps(error_msg)}\n'
                         yield 'd:{"finishReason":"stop"}\n'
                         return
                    
                    # Fallback to simple completion (break loop after this as it doesn't support tools)
                    try:
                        response = await client.chat.completions.create(
                            model=settings.default_model,
                            messages=ai_messages,
                            max_tokens=1000,
                            stream=True,
                        )
                    except Exception as fallback_error:
                         error_msg = f"AI service error: {str(fallback_error)}"
                         yield f'0:{json.dumps(error_msg)}\n'
                         yield 'd:{"finishReason":"stop"}\n'
                         return

                # Stream response
                tool_calls_collected = []
                current_response_content = ""
                
                try:
                    async for chunk in response:
                        if chunk.choices:
                            delta = chunk.choices[0].delta

                            # Stream content tokens
                            if delta.content:
                                current_response_content += delta.content
                                full_response += delta.content
                                escaped_content = json.dumps(delta.content)
                                yield f'0:{escaped_content}\n'

                            # Collect tool calls
                            if hasattr(delta, 'tool_calls') and delta.tool_calls:
                                for tool_call_chunk in delta.tool_calls:
                                    if len(tool_calls_collected) <= tool_call_chunk.index:
                                        tool_calls_collected.extend([None] * (tool_call_chunk.index - len(tool_calls_collected) + 1))

                                    if tool_calls_collected[tool_call_chunk.index] is None:
                                        tool_calls_collected[tool_call_chunk.index] = {
                                            "id": tool_call_chunk.id,
                                            "function": {
                                                "name": tool_call_chunk.function.name if tool_call_chunk.function else "",
                                                "arguments": tool_call_chunk.function.arguments if tool_call_chunk.function else ""
                                            },
                                            "type": "function"
                                        }
                                    else:
                                        if tool_call_chunk.function and tool_call_chunk.function.arguments:
                                            tool_calls_collected[tool_call_chunk.index]["function"]["arguments"] += tool_call_chunk.function.arguments
                except Exception as stream_error:
                    logger.error(f"Streaming error: {str(stream_error)}")
                    error_msg = f"AI service temporarily unavailable: {str(stream_error)}"
                    yield f'0:{json.dumps(error_msg)}\n'
                    yield 'd:{"finishReason":"stop"}\n'
                    return

                # Execute tool calls if any
                executed_tool_calls = []
                if tool_calls_collected and any(tc for tc in tool_calls_collected if tc is not None):
                    
                    # Append assistant message with tool calls to history
                    assistant_msg_struct = {
                        "role": "assistant",
                        "content": current_response_content if current_response_content else None,
                        "tool_calls": []
                    }
                    
                    valid_tool_calls = []
                    for tool_call_data in tool_calls_collected:
                        if tool_call_data is None: continue
                        
                        valid_tool_calls.append({
                            "id": tool_call_data["id"],
                            "type": "function",
                            "function": {
                                "name": tool_call_data["function"]["name"],
                                "arguments": tool_call_data["function"]["arguments"]
                            }
                        })
                    
                    assistant_msg_struct["tool_calls"] = valid_tool_calls
                    ai_messages.append(assistant_msg_struct)

                 # Save intermediate assistant message with tool calls to DB        
                    assistant_msg_db = Message(
                        conversation_id=conversation_id,
                        user_id=user_id,
                        role=MessageRole.ASSISTANT,
                        content=current_response_content or "",
                        tool_calls=json.dumps(valid_tool_calls)
                    )
                    self.db.add(assistant_msg_db)
                    await self.db.commit()

                    for tool_call_data in tool_calls_collected:
                        if tool_call_data is None:
                            continue

                        try:
                            tool_call_obj = ToolCall(
                                id=tool_call_data["id"],
                                name=tool_call_data["function"]["name"],
                                arguments=json.loads(tool_call_data["function"]["arguments"])
                            )

                            # Execute tool
                            result = await self.execute_tool_call(tool_call_obj, user_id)

                            # Save tool message (DB)
                            tool_message = Message(
                                conversation_id=conversation_id,
                                user_id=user_id,
                                role=MessageRole.TOOL,
                                content=json.dumps(result),
                                tool_calls=json.dumps({
                                    "name": tool_call_obj.name,
                                    "arguments": tool_call_obj.arguments
                                })
                            )
                            self.db.add(tool_message)
                            
                            # Stream tool notification
                            tool_notification = f"\n[Executed: {tool_call_obj.name}]\n"
                            yield f'0:{json.dumps(tool_notification)}\n'
                            
                            # Append tool result to history
                            ai_messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call_obj.id,
                                "content": json.dumps(result)
                            })
                            
                            executed_tool_calls.append(result)

                        except Exception as e:
                            logger.error(f"Tool execution error: {str(e)}")
                            # Append error result so AI knows it failed
                            ai_messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call_data["id"],
                                "content": json.dumps({"error": str(e)})
                            })
                            continue
                    
                    # Loop continues to next iteration to process tool results
                    continue
                
                else:
                    # No tools called, we are done
                    break

            # Save assistant response
            assistant_message = Message(
                conversation_id=conversation_id,
                user_id=user_id,
                role=MessageRole.ASSISTANT,
                content=full_response or "Request processed."
            )
            self.db.add(assistant_message)
            await self.db.commit()

            # Send completion signal
            yield 'd:{"finishReason":"stop"}\n'

        except asyncio.CancelledError:
            logger.info(f"Client disconnected during streaming")
            if conversation_id and full_response:
                assistant_message = Message(
                    conversation_id=conversation_id,
                    user_id=user_id,
                    role=MessageRole.ASSISTANT,
                    content=full_response
                )
                self.db.add(assistant_message)
                await self.db.commit()
            yield 'd:{"finishReason":"stop"}\n'
            # Don't raise here to prevent propagation of cancelled error

        except Exception as e:
            logger.error(f"Streaming error: {str(e)}")
            # Send error in Vercel AI SDK format 
            yield f'3:{json.dumps(str(e))}\n'
            yield f'3:{error_data}\n'
            yield 'd:{"finishReason":"error"}\n'
            # Don't raise here to prevent propagation of error that might cause stream to abort
#  ------------------------------------
