from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime, timedelta
from typing import List, Optional
from app.models.task_advanced import Task, Message, Conversation
from app.database.connection import get_session
from app.schemas.task_schemas import TaskCreate, TaskUpdate, TaskResponse
from uuid import UUID

router = APIRouter(prefix="/api", tags=["tasks"])

@router.post("/users/{user_id}/tasks", response_model=TaskResponse)
def create_task(
    user_id: str,
    task_data: TaskCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new task with advanced features like due dates, priorities, categories, and recurrence
    """
    # Validate recurrence pattern if provided
    if task_data.is_recurring and task_data.recurrence_pattern:
        valid_patterns = ["daily", "weekly", "monthly", "yearly"]
        if task_data.recurrence_pattern.lower() not in valid_patterns:
            raise HTTPException(status_code=400, detail="Invalid recurrence pattern")

        # Calculate next occurrence based on pattern
        next_occurrence = calculate_next_occurrence(datetime.utcnow(), task_data.recurrence_pattern)
    else:
        next_occurrence = None

    # Create task object
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority or "medium",
        due_date=task_data.due_date,
        reminder_time=task_data.reminder_time,
        category=task_data.category,
        is_recurring=task_data.is_recurring or False,
        recurrence_pattern=task_data.recurrence_pattern,
        next_occurrence=next_occurrence,
        end_recurrence=task_data.end_recurrence
    )

    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse.from_orm(task)

@router.get("/users/{user_id}/tasks", response_model=List[TaskResponse])
def get_tasks(
    user_id: str,
    status: Optional[str] = Query(None, description="Filter by status: all, pending, completed"),
    priority: Optional[str] = Query(None, description="Filter by priority: low, medium, high"),
    category: Optional[str] = Query(None, description="Filter by category/tag"),
    due_date_from: Optional[datetime] = Query(None, description="Filter tasks due after this date"),
    due_date_to: Optional[datetime] = Query(None, description="Filter tasks due before this date"),
    sort_by: Optional[str] = Query("created_at", description="Sort by: created_at, due_date, title, priority"),
    sort_order: Optional[str] = Query("asc", description="Sort order: asc, desc"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    session: Session = Depends(get_session)
):
    """
    Get tasks with advanced filtering, searching, and sorting capabilities
    """
    query = select(Task).where(Task.user_id == user_id)

    # Apply status filter
    if status and status != "all":
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

    # Apply priority filter
    if priority:
        query = query.where(Task.priority == priority)

    # Apply category filter
    if category:
        query = query.where(Task.category == category)

    # Apply due date filters
    if due_date_from:
        query = query.where(Task.due_date >= due_date_from)
    if due_date_to:
        query = query.where(Task.due_date <= due_date_to)

    # Apply search
    if search:
        search_filter = f"%{search}%"
        query = query.where(
            (Task.title.ilike(search_filter)) |
            (Task.description.ilike(search_filter))
        )

    # Apply sorting
    if sort_by == "due_date":
        if sort_order == "desc":
            query = query.order_by(Task.due_date.desc())
        else:
            query = query.order_by(Task.due_date.asc())
    elif sort_by == "priority":
        if sort_order == "desc":
            query = query.order_by(Task.priority.desc())
        else:
            query = query.order_by(Task.priority.asc())
    elif sort_by == "title":
        if sort_order == "desc":
            query = query.order_by(Task.title.desc())
        else:
            query = query.order_by(Task.title.asc())
    else:  # Default to created_at
        if sort_order == "desc":
            query = query.order_by(Task.created_at.desc())
        else:
            query = query.order_by(Task.created_at.asc())

    tasks = session.exec(query).all()
    return [TaskResponse.from_orm(task) for task in tasks]

@router.put("/users/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    user_id: str,
    task_id: int,
    task_data: TaskUpdate,
    session: Session = Depends(get_session)
):
    """
    Update a task with advanced features
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this task")

    # Update fields if provided
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.priority is not None:
        task.priority = task_data.priority
    if task_data.due_date is not None:
        task.due_date = task_data.due_date
    if task_data.reminder_time is not None:
        task.reminder_time = task_data.reminder_time
    if task_data.category is not None:
        task.category = task_data.category
    if task_data.completed is not None:
        task.completed = task_data.completed
    if task_data.is_recurring is not None:
        task.is_recurring = task_data.is_recurring
    if task_data.recurrence_pattern is not None:
        task.recurrence_pattern = task_data.recurrence_pattern
    if task_data.end_recurrence is not None:
        task.end_recurrence = task_data.end_recurrence

    # If recurrence pattern changed, recalculate next occurrence
    if task_data.recurrence_pattern and task.is_recurring:
        task.next_occurrence = calculate_next_occurrence(datetime.utcnow(), task_data.recurrence_pattern)

    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
    session.refresh(task)

    return TaskResponse.from_orm(task)

def calculate_next_occurrence(current_date: datetime, pattern: str) -> Optional[datetime]:
    """
    Calculate the next occurrence date based on the recurrence pattern
    """
    if not pattern:
        return None

    pattern_lower = pattern.lower()

    if pattern_lower == "daily":
        return current_date + timedelta(days=1)
    elif pattern_lower == "weekly":
        return current_date + timedelta(weeks=1)
    elif pattern_lower == "monthly":
        # Add one month (approximately)
        if current_date.month == 12:
            return current_date.replace(year=current_date.year + 1, month=1)
        else:
            return current_date.replace(month=current_date.month + 1)
    elif pattern_lower == "yearly":
        # Add one year
        return current_date.replace(year=current_date.year + 1)
    else:
        return None

@router.post("/users/{user_id}/tasks/{task_id}/generate-next-occurrence")
def generate_next_occurrence(
    user_id: str,
    task_id: int,
    session: Session = Depends(get_session)
):
    """
    Generate the next occurrence of a recurring task
    """
    original_task = session.get(Task, task_id)
    if not original_task:
        raise HTTPException(status_code=404, detail="Original task not found")

    if original_task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this task")

    if not original_task.is_recurring:
        raise HTTPException(status_code=400, detail="Task is not recurring")

    # Check if recurrence should end
    if original_task.end_recurrence and datetime.utcnow() > original_task.end_recurrence:
        # Disable recurrence for the parent task
        original_task.is_recurring = False
        session.add(original_task)
        session.commit()
        return {"message": "Recurrence ended for this task"}

    # Create new occurrence based on the original task
    new_task = Task(
        user_id=original_task.user_id,
        title=original_task.title,
        description=original_task.description,
        priority=original_task.priority,
        due_date=original_task.next_occurrence,  # Use the calculated next occurrence
        reminder_time=original_task.reminder_time,
        category=original_task.category,
        is_recurring=original_task.is_recurring,
        recurrence_pattern=original_task.recurrence_pattern,
        parent_task_id=original_task.id,  # Link to parent task
        end_recurrence=original_task.end_recurrence
    )

    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    # Calculate next occurrence for the parent task
    if original_task.recurrence_pattern:
        original_task.next_occurrence = calculate_next_occurrence(
            original_task.next_occurrence or datetime.utcnow(),
            original_task.recurrence_pattern
        )

        # Check if recurrence should end after creating this occurrence
        if original_task.end_recurrence and original_task.next_occurrence > original_task.end_recurrence:
            original_task.is_recurring = False

        session.add(original_task)
        session.commit()

    return {"message": "Next occurrence created", "new_task_id": new_task.id}

# Additional endpoints for reminders and scheduling would go here