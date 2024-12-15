import threading
import time
from typing import Dict, List, Optional

class MessageQueue:
    def __init__(self):
        # Dictionary to store queues for different queue names
        self._queues: Dict[str, List[dict]] = {}
        # Dictionary to store thread locks for each queue
        self._locks: Dict[str, threading.Lock] = {}

    def enqueue(self, queue_name: str, message: dict) -> None:
        """
        Add a message to a specific queue.
        Creates the queue if it doesn't exist.
        
        :param queue_name: Name of the queue
        :param message: Message to be added
        """
        # Create queue and lock if not exists
        if queue_name not in self._locks:
            self._locks[queue_name] = threading.Lock()
            self._queues[queue_name] = []

        # Thread-safe enqueue
        with self._locks[queue_name]:
            self._queues[queue_name].append(message)

    def dequeue(self, queue_name: str, timeout: float = 10.0) -> Optional[dict]:
        """
        Remove and return the first message from a queue.
        Waits for a message if queue is empty until timeout.
        
        :param queue_name: Name of the queue
        :param timeout: Timeout in milliseconds
        :return: Message or None if no message within timeout
        """
        # Check if queue exists
        if queue_name not in self._locks:
            return None

        # Wait for message with timeout
        start_time = time.time()
        while time.time() - start_time < timeout / 1000.0:
            with self._locks[queue_name]:
                if self._queues[queue_name]:
                    return self._queues[queue_name].pop(0)
            time.sleep(0.1)

        return None

    def get_queue_stats(self) -> Dict[str, int]:
        """
        Get the number of messages in each queue.
        
        :return: Dictionary of queue names and their message counts
        """
        return {name: len(queue) for name, queue in self._queues.items()}
