import json
from kafka import KafkaConsumer
from threading import Thread
import logging
from typing import Callable, Dict, Any
from sqlmodel import Session
from ..database.connection import get_session
from ..models.task_advanced import Task

logger = logging.getLogger(__name__)

class KafkaTaskConsumer:
    def __init__(self, bootstrap_servers: str = "localhost:9092"):
        """
        Initialize Kafka consumer for task events
        """
        try:
            self.consumer = KafkaConsumer(
                'task-events',
                'reminders',
                'task-updates',
                bootstrap_servers=bootstrap_servers,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                key_deserializer=lambda k: k.decode('utf-8') if k else None,
                group_id='todo-consumer-group',
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                request_timeout_ms=5000,  # Fail faster if brokers are down
                connection_timeout_ms=5000
            )
            logger.info(f"Kafka consumer initialized with servers: {bootstrap_servers}")
        except Exception as e:
            logger.warning(f"Failed to initialize Kafka consumer: {e}. Consumer features will be disabled.")
            self.consumer = None

        # Define handlers for different event types
        self.handlers: Dict[str, Callable] = {
            'task-events': self.handle_task_event,
            'reminders': self.handle_reminder_event,
            'task-updates': self.handle_task_update_event
        }

        self.running = False
        self.consumer_thread = None

    def start_consuming(self):
        """
        Start consuming messages from Kafka
        """
        if self.running or not self.consumer:
            if not self.consumer:
                logger.warning("Kafka consumer not initialized. Cannot start consuming.")
            return

        self.running = True
        self.consumer_thread = Thread(target=self._consume_messages, daemon=True)
        self.consumer_thread.start()
        logger.info("Started consuming messages from Kafka")

    def _consume_messages(self):
        """
        Internal method to consume messages
        """
        try:
            for message in self.consumer:
                if not self.running:
                    break

                topic = message.topic
                key = message.key
                value = message.value

                logger.info(f"Received message from topic {topic}, key: {key}")

                # Route to appropriate handler
                handler = self.handlers.get(topic)
                if handler:
                    try:
                        handler(value)
                    except Exception as e:
                        logger.error(f"Error handling message from {topic}: {e}")
                        # In a real system, you might want to send to a dead letter queue
                else:
                    logger.warning(f"No handler found for topic: {topic}")

        except Exception as e:
            logger.error(f"Error in consumer loop: {e}")
        finally:
            logger.info("Kafka consumer loop ended")

    def handle_task_event(self, event_data: Dict[str, Any]):
        """
        Handle task-related events
        """
        event_type = event_data.get('event_type')
        task_id = event_data.get('task_id')
        user_id = event_data.get('user_id')

        logger.info(f"Handling task event: {event_type} for task {task_id} by user {user_id}")

        # In a real implementation, this would update audit logs, trigger notifications, etc.
        if event_type == 'created':
            logger.info(f"Task {task_id} was created for user {user_id}")
            # Could trigger notifications, update dashboards, etc.
        elif event_type == 'updated':
            logger.info(f"Task {task_id} was updated for user {user_id}")
        elif event_type == 'completed':
            logger.info(f"Task {task_id} was completed by user {user_id}")
            # Could trigger next steps in workflow
        elif event_type == 'deleted':
            logger.info(f"Task {task_id} was deleted by user {user_id}")
        elif event_type == 'recurring_created':
            logger.info(f"Recurring occurrence of task {task_id} was created for user {user_id}")
            # Could send notifications about new recurring task

    def handle_reminder_event(self, event_data: Dict[str, Any]):
        """
        Handle reminder-related events
        """
        task_id = event_data.get('task_id')
        title = event_data.get('title')
        user_id = event_data.get('user_id')
        remind_at = event_data.get('remind_at')

        logger.info(f"Handling reminder for task {task_id} ({title}) for user {user_id} at {remind_at}")

        # In a real implementation, this would send push notifications, emails, etc.
        # For now, just log the reminder
        logger.info(f"REMINDER: Task '{title}' (ID: {task_id}) is due soon!")

        # In a real system, you would call notification services here
        # notification_service.send_reminder(user_id, task_id, title)

    def handle_task_update_event(self, event_data: Dict[str, Any]):
        """
        Handle task update events (for real-time sync across clients)
        """
        task_id = event_data.get('task_id')
        user_id = event_data.get('user_id')
        update_type = event_data.get('update_type')
        changes = event_data.get('changes', {})

        logger.info(f"Handling task update: {update_type} for task {task_id} by user {user_id}")

        # In a real implementation, this would broadcast updates to all connected clients
        # via WebSocket or similar real-time communication
        logger.info(f"Task {task_id} was updated ({update_type}): {changes}")

        # Could trigger WebSocket broadcasts to update UI in real-time
        # websocket_service.broadcast_update(user_id, task_id, update_type, changes)

    def stop_consuming(self):
        """
        Stop consuming messages
        """
        self.running = False
        if self.consumer:
            self.consumer.close()
        if self.consumer_thread:
            self.consumer_thread.join(timeout=5)  # Wait up to 5 seconds for thread to finish
        logger.info("Stopped consuming messages from Kafka")

# Global instance of Kafka consumer
kafka_consumer = None

def get_kafka_consumer(bootstrap_servers: str = "localhost:9092") -> KafkaTaskConsumer:
    """
    Get or create a singleton instance of Kafka consumer
    """
    global kafka_consumer
    if kafka_consumer is None:
        kafka_consumer = KafkaTaskConsumer(bootstrap_servers)
    return kafka_consumer