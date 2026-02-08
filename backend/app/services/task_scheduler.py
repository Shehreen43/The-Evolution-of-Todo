from datetime import datetime, timedelta
from sqlmodel import Session, select
from ..models.task_advanced import Task
from ..database.connection import get_session
from typing import List
import asyncio
import logging

logger = logging.getLogger(__name__)

class TaskSchedulerService:
    def __init__(self, session: Session):
        self.session = session

    def check_and_generate_recurring_tasks(self):
        """
        Check for recurring tasks that need to generate new occurrences
        """
        logger.info("Checking for recurring tasks to generate...")

        # Find tasks that are recurring and have a next occurrence date that is today or in the past
        recurring_tasks = self.session.exec(
            select(Task)
            .where(Task.is_recurring == True)
            .where(Task.next_occurrence <= datetime.utcnow())
            .where(Task.completed == False)
        ).all()

        generated_tasks = []
        for task in recurring_tasks:
            # Create a new occurrence of the task
            new_task = Task(
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                priority=task.priority,
                due_date=task.next_occurrence,
                reminder_time=task.reminder_time,
                category=task.category,
                is_recurring=task.is_recurring,
                recurrence_pattern=task.recurrence_pattern,
                parent_task_id=task.id,
                end_recurrence=task.end_recurrence
            )

            # Add the new task to the session
            self.session.add(new_task)
            self.session.flush()  # Get the ID without committing

            # Update the parent task's next occurrence
            if task.recurrence_pattern:
                next_occurrence = self.calculate_next_occurrence(
                    task.next_occurrence or datetime.utcnow(),
                    task.recurrence_pattern
                )

                # Check if recurrence should end
                if task.end_recurrence and next_occurrence > task.end_recurrence:
                    task.is_recurring = False
                else:
                    task.next_occurrence = next_occurrence

            self.session.add(task)
            generated_tasks.append(new_task.id)

        # Commit all changes
        self.session.commit()

        logger.info(f"Generated {len(generated_tasks)} new recurring task occurrences: {generated_tasks}")
        return generated_tasks

    def check_and_send_reminders(self):
        """
        Check for tasks that need to send reminders
        """
        logger.info("Checking for tasks with upcoming reminders...")

        # Find tasks with reminder times that are now or in the past
        tasks_with_reminders = self.session.exec(
            select(Task)
            .where(Task.reminder_time <= datetime.utcnow())
            .where(Task.completed == False)
        ).all()

        reminded_tasks = []
        for task in tasks_with_reminders:
            # In a real implementation, this would send a notification
            # For now, we'll just log it
            logger.info(f"Reminder needed for task {task.id}: {task.title}")
            reminded_tasks.append(task.id)

            # Mark the reminder as sent by clearing the reminder time
            # In a real system, you might want to keep track of sent reminders differently
            task.reminder_time = None
            self.session.add(task)

        self.session.commit()

        logger.info(f"Processed reminders for {len(reminded_tasks)} tasks: {reminded_tasks}")
        return reminded_tasks

    def calculate_next_occurrence(self, current_date: datetime, pattern: str) -> datetime:
        """
        Calculate the next occurrence date based on the recurrence pattern
        """
        if not pattern:
            return current_date + timedelta(days=1)  # Default to daily

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
            # Default to daily if invalid pattern
            return current_date + timedelta(days=1)

    def get_upcoming_tasks(self, user_id: str, days_ahead: int = 7) -> List[Task]:
        """
        Get tasks that are due in the next N days
        """
        cutoff_date = datetime.utcnow() + timedelta(days=days_ahead)

        upcoming_tasks = self.session.exec(
            select(Task)
            .where(Task.user_id == user_id)
            .where(Task.due_date <= cutoff_date)
            .where(Task.completed == False)
            .where(Task.due_date >= datetime.utcnow())
            .order_by(Task.due_date.asc())
        ).all()

        return upcoming_tasks

    def get_overdue_tasks(self, user_id: str) -> List[Task]:
        """
        Get tasks that are overdue (past due date and not completed)
        """
        overdue_tasks = self.session.exec(
            select(Task)
            .where(Task.user_id == user_id)
            .where(Task.due_date < datetime.utcnow())
            .where(Task.completed == False)
            .order_by(Task.due_date.asc())
        ).all()

        return overdue_tasks

# Background task scheduler
class BackgroundTaskScheduler:
    def __init__(self):
        self.is_running = False

    async def start_scheduler(self):
        """
        Start the background task scheduler
        """
        if self.is_running:
            return

        self.is_running = True
        logger.info("Background task scheduler started")

        while self.is_running:
            try:
                # Create a new session for this cycle
                with get_session() as session:
                    scheduler_service = TaskSchedulerService(session)

                    # Run recurring task generation
                    scheduler_service.check_and_generate_recurring_tasks()

                    # Run reminder checks
                    scheduler_service.check_and_send_reminders()

            except Exception as e:
                logger.error(f"Error in background scheduler: {e}")

            # Wait 1 hour before next check
            await asyncio.sleep(3600)  # 1 hour

    def stop_scheduler(self):
        """
        Stop the background task scheduler
        """
        self.is_running = False
        logger.info("Background task scheduler stopped")

# Global instance of the scheduler
scheduler = BackgroundTaskScheduler()