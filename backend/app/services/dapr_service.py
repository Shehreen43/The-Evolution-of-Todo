import httpx
import json
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DaprService:
    def __init__(self, dapr_http_port: int = 3500, dapr_grpc_port: int = 50001):
        """
        Initialize Dapr service client
        """
        self.dapr_http_port = dapr_http_port
        self.dapr_grpc_port = dapr_grpc_port
        self.base_url = f"http://localhost:{dapr_http_port}"

    async def publish_event(self, pubsub_name: str, topic_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Publish an event to a Dapr pub/sub component

        Args:
            pubsub_name: Name of the pub/sub component (e.g., 'kafka-pubsub')
            topic_name: Name of the topic to publish to
            data: Data to publish

        Returns:
            Response from Dapr
        """
        url = f"{self.base_url}/v1.0/publish/{pubsub_name}/{topic_name}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data)

                if response.status_code == 200:
                    logger.info(f"Successfully published to {pubsub_name}/{topic_name}")
                    return {"success": True, "message": "Published successfully"}
                else:
                    logger.error(f"Failed to publish to {pubsub_name}/{topic_name}. Status: {response.status_code}, Body: {response.text}")
                    return {"success": False, "error": response.text, "status_code": response.status_code}

        except Exception as e:
            logger.error(f"Exception publishing to {pubsub_name}/{topic_name}: {str(e)}")
            return {"success": False, "error": str(e)}

    async def save_state(self, store_name: str, key: str, value: Any, etag: Optional[str] = None) -> Dict[str, Any]:
        """
        Save state to a Dapr state store

        Args:
            store_name: Name of the state store component
            key: Key for the state
            value: Value to store
            etag: Optional etag for concurrency control

        Returns:
            Response from Dapr
        """
        url = f"{self.base_url}/v1.0/state/{store_name}"

        state_item = {
            "key": key,
            "value": value
        }

        if etag:
            state_item["etag"] = etag

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=[state_item])

                if response.status_code == 204:
                    logger.info(f"Successfully saved state for key {key} in {store_name}")
                    return {"success": True, "message": "State saved successfully"}
                else:
                    logger.error(f"Failed to save state for key {key}. Status: {response.status_code}, Body: {response.text}")
                    return {"success": False, "error": response.text}

        except Exception as e:
            logger.error(f"Exception saving state for key {key}: {str(e)}")
            return {"success": False, "error": str(e)}

    async def get_state(self, store_name: str, key: str, consistency: str = " eventual") -> Any:
        """
        Get state from a Dapr state store

        Args:
            store_name: Name of the state store component
            key: Key for the state
            consistency: Consistency level ("eventual" or "strong")

        Returns:
            Retrieved state value
        """
        url = f"{self.base_url}/v1.0/state/{store_name}/{key}?consistency={consistency}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)

                if response.status_code == 200:
                    logger.info(f"Successfully retrieved state for key {key}")
                    return response.json()
                elif response.status_code == 404:
                    logger.info(f"State not found for key {key}")
                    return None
                else:
                    logger.error(f"Failed to get state for key {key}. Status: {response.status_code}, Body: {response.text}")
                    return None

        except Exception as e:
            logger.error(f"Exception getting state for key {key}: {str(e)}")
            return None

    async def invoke_service(self, app_id: str, method: str, data: Optional[Dict[str, Any]] = None, http_verb: str = "POST") -> Any:
        """
        Invoke another service via Dapr service invocation

        Args:
            app_id: ID of the target service
            method: Method to invoke on the target service
            data: Optional data to send
            http_verb: HTTP verb to use (GET, POST, PUT, DELETE)

        Returns:
            Response from the target service
        """
        url = f"{self.base_url}/v1.0/invoke/{app_id}/method/{method}"

        try:
            async with httpx.AsyncClient() as client:
                if http_verb.upper() == "GET":
                    response = await client.get(url)
                elif http_verb.upper() == "POST":
                    response = await client.post(url, json=data)
                elif http_verb.upper() == "PUT":
                    response = await client.put(url, json=data)
                elif http_verb.upper() == "DELETE":
                    response = await client.delete(url)
                else:
                    raise ValueError(f"Unsupported HTTP verb: {http_verb}")

                if response.status_code in [200, 201, 204]:
                    try:
                        return response.json()
                    except:
                        # If response is not JSON, return as text
                        return response.text
                else:
                    logger.error(f"Failed to invoke service {app_id}/{method}. Status: {response.status_code}, Body: {response.text}")
                    return {"error": response.text, "status_code": response.status_code}

        except Exception as e:
            logger.error(f"Exception invoking service {app_id}/{method}: {str(e)}")
            return {"error": str(e)}

    async def get_secret(self, store_name: str, key: str, metadata: Optional[Dict[str, str]] = None) -> Any:
        """
        Get a secret from a Dapr secret store

        Args:
            store_name: Name of the secret store component
            key: Key for the secret
            metadata: Optional metadata for the request

        Returns:
            Secret value
        """
        url = f"{self.base_url}/v1.0/secrets/{store_name}/{key}"

        if metadata:
            # Convert metadata to query string
            query_params = "&".join([f"metadata.{k}={v}" for k, v in metadata.items()])
            url += f"?{query_params}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)

                if response.status_code == 200:
                    secrets = response.json()
                    logger.info(f"Successfully retrieved secret for key {key}")
                    # Return the actual secret value (not the wrapper)
                    return secrets.get(key)
                else:
                    logger.error(f"Failed to get secret for key {key}. Status: {response.status_code}, Body: {response.text}")
                    return None

        except Exception as e:
            logger.error(f"Exception getting secret for key {key}: {str(e)}")
            return None

    async def schedule_job(self, job_name: str, due_time: str, data: Optional[Dict[str, Any]] = None, period: Optional[str] = None) -> Dict[str, Any]:
        """
        Schedule a job using Dapr Jobs API (alpha)

        Args:
            job_name: Name of the job
            due_time: When the job should run (ISO 8601 duration or timestamp)
            data: Optional data to pass to the job
            period: Optional period for recurring jobs (ISO 8601 duration)

        Returns:
            Response from Dapr
        """
        url = f"{self.base_url}/v1.0-alpha1/jobs/{job_name}"

        payload = {
            "dueTime": due_time,
            "data": data or {}
        }

        if period:
            payload["period"] = period

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)

                if response.status_code == 200:
                    logger.info(f"Successfully scheduled job {job_name}")
                    return {"success": True, "message": f"Job {job_name} scheduled successfully"}
                else:
                    logger.error(f"Failed to schedule job {job_name}. Status: {response.status_code}, Body: {response.text}")
                    return {"success": False, "error": response.text}

        except Exception as e:
            logger.error(f"Exception scheduling job {job_name}: {str(e)}")
            return {"success": False, "error": str(e)}

    async def publish_task_event_via_dapr(self, event_type: str, task_data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Publish a task event using Dapr pub/sub instead of direct Kafka
        """
        event = {
            'event_type': event_type,
            'task_id': task_data.get('id'),
            'task_data': task_data,
            'user_id': user_id,
            'timestamp': datetime.utcnow().isoformat()
        }

        # Publish to the task-events topic using Dapr
        return await self.publish_event("kafka-pubsub", "task-events", event)

    async def publish_reminder_event_via_dapr(self, task_id: int, title: str, due_at: str, remind_at: str, user_id: str) -> Dict[str, Any]:
        """
        Publish a reminder event using Dapr pub/sub
        """
        event = {
            'task_id': task_id,
            'title': title,
            'due_at': due_at,
            'remind_at': remind_at,
            'user_id': user_id,
            'timestamp': datetime.utcnow().isoformat()
        }

        # Publish to the reminders topic using Dapr
        return await self.publish_event("kafka-pubsub", "reminders", event)

# Global instance of Dapr service
dapr_service = None

def get_dapr_service(dapr_http_port: int = 3500) -> DaprService:
    """
    Get or create a singleton instance of Dapr service
    """
    global dapr_service
    if dapr_service is None:
        dapr_service = DaprService(dapr_http_port)
    return dapr_service