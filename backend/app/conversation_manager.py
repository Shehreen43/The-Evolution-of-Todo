"""
Conversation manager for the AI Chatbot integration.

This module handles conversation creation, retrieval, and management for the chatbot.
"""

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.models.conversation import Conversation
from app.models.message import Message


async def create_conversation(session: AsyncSession, user_id: str, title: Optional[str] = None) -> Conversation:
    """
    Create a new conversation for the given user.

    Args:
        session: Database session
        user_id: User identifier
        title: Optional title for the conversation

    Returns:
        Created Conversation object
    """
    if title is None:
        title = "New Conversation"

    conversation = Conversation(user_id=user_id, title=title)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation


async def get_conversation(session: AsyncSession, conversation_id: int, user_id: str) -> Optional[Conversation]:
    """
    Retrieve a conversation by ID for the specified user.

    Args:
        session: Database session
        conversation_id: ID of the conversation to retrieve
        user_id: User identifier

    Returns:
        Conversation object if found and belongs to user, None otherwise
    """
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_conversation_history(session: AsyncSession, conversation_id: int) -> List[Message]:
    """
    Retrieve the message history for a conversation.

    Args:
        session: Database session
        conversation_id: ID of the conversation

    Returns:
        List of messages in chronological order
    """
    statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc())

    result = await session.execute(statement)
    messages = result.scalars().all()
    return messages