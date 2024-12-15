import time
from collections import deque

class QueueManager:
    def __init__(self):
        self.queues = {}  # A dictionary to store queues, where each queue is a deque (double-ended queue)

    def add_message(self, queue_name, message):
        # If the queue doesn't exist, create a new one
        if queue_name not in self.queues:
            self.queues[queue_name] = deque()
        # Add the message to the queue
        self.queues[queue_name].append(message)

    def get_message(self, queue_name, timeout=10):
        # If the queue doesn't exist or is empty, return None
        if queue_name not in self.queues or not self.queues[queue_name]:
            return None

        start_time = time.time()
        # Wait until the timeout expires or a message is available
        while time.time() - start_time < timeout:
            if self.queues[queue_name]:
                # Return the first message from the queue
                return self.queues[queue_name].popleft()

        # If the timeout expires without a message, return None
        return None
