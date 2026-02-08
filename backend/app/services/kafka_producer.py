import json
from typing import Dict, Any
from kafka import KafkaProducer
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class KafkaTaskProducer:
    def __init__(self, bootstrap_servers: str = "localhost:9092"):
        """
        Initialize Kafka producer for task events
        """
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                acks='all',  # Wait for all replicas to acknowledge
                retries=3,
                linger_ms=5,  # Small delay to batch messages
                batch_size=16384  # Batch size in bytes
            )
            logger.info(f"Kafka producer initialized with servers: {bootstrap_servers}")
        except Exception as e:
            logger.warning(f"Failed to initialize Kafka producer: {e}. Kafka features will be disabled.")
            self.producer = None

        # Define topic names
        self.TASK_EVENTS_TOPIC = 'task-events'
        self.REMINDERS_TOPIC = 'reminders'
        self.TASK_UPDATES_TOPIC = 'task-updates'

    def send_task_event(self, event_type: str, task_data: Dict[str, Any], user_id: str):
        """
        Send a task event to Kafka

        Args:
            event_type: Type of event ('created', 'updated', 'completed', 'deleted', 'recurring_created')
            task_data: Dictionary containing task information
            user_id: ID of the user who triggered the event
        """
        event = {
            'event_type': event_type,
            'task_id': task_data.get('id'),
            'task_data': task_data,
            'user_id': user_id,
            'timestamp': datetime.utcnow().isoformat()
        }

        if not self.producer:
            logger.warning("Kafka producer not initialized. Skipping task event.")
            return

        try:
            future = self.producer.send(self.TASK_EVENTS_TOPIC, key=str(user_id), value=event)
            # Block for confirmation
            record_metadata = future.get(timeout=10)
            logger.info(f"Task event sent to topic {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")
        except Exception as e:
            logger.error(f"Failed to send task event: {e}")

    def send_reminder_event(self, task_id: int, title: str, due_at: str, remind_at: str, user_id: str):
        """
        Send a reminder event to Kafka

        Args:
            task_id: ID of the task
            title: Title of the task
            due_at: When the task is due
            remind_at: When to send the reminder
            user_id: ID of the user who owns the task
        """
        event = {
            'task_id': task_id,
            'title': title,
            'due_at': due_at,
            'remind_at': remind_at,
            'user_id': user_id,
            'timestamp': datetime.utcnow().isoformat()
        }

        if not self.producer:
            logger.warning("Kafka producer not initialized. Skipping reminder event.")
            return

        try:
            future = self.producer.send(self.REMINDERS_TOPIC, key=str(user_id), value=event)
            record_metadata = future.get(timeout=10)
            logger.info(f"Reminder event sent to topic {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")
        except Exception as e:
            logger.error(f"Failed to send reminder event: {e}")

    def send_task_update_event(self, task_id: int, user_id: str, update_type: str, changes: Dict[str, Any]):
        """
        Send a task update event to Kafka for real-time sync

        Args:
            task_id: ID of the task
            user_id: ID of the user who made the update
            update_type: Type of update ('status_change', 'details_updated', 'priority_changed', etc.)
            changes: Dictionary containing the specific changes made
        """
        event = {
            'task_id': task_id,
            'user_id': user_id,
            'update_type': update_type,
            'changes': changes,
            'timestamp': datetime.utcnow().isoformat()
        }

        if not self.producer:
            logger.warning("Kafka producer not initialized. Skipping task update event.")
            return

        try:
            future = self.producer.send(self.TASK_UPDATES_TOPIC, key=f"{user_id}:{task_id}", value=event)
            record_metadata = future.get(timeout=10)
            logger.info(f"Task update event sent to topic {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}")
        except Exception as e:
            logger.error(f"Failed to send task update event: {e}")

    def close(self):
        """
        Close the Kafka producer
        """
        if self.producer:
            self.producer.close()

# Global instance of Kafka producer
kafka_producer = None

def get_kafka_producer(bootstrap_servers: str = "localhost:9092") -> KafkaTaskProducer:
    """
    Get or create a singleton instance of Kafka producer
    """
    global kafka_producer
    if kafka_producer is None:
        kafka_producer = KafkaTaskProducer(bootstrap_servers)
    return kafka_producer