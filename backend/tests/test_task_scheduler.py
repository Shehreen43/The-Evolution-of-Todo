from app.services.task_scheduler import TaskSchedulerService

def test_task_scheduler_import():
    assert TaskSchedulerService is not None
